import os
import re
import shutil
from abc import ABC, abstractmethod
from io import BytesIO

import pytz
import pandas as pd
import xlrd
from loguru import logger
from minio import Minio
from pathlib import Path
from datetime import datetime

# prefix components:
from minio.select import SelectRequest, CSVInputSerialization, CSVOutputSerialization
from minio.commonconfig import CopySource

space = '    '
branch = '│   '
# pointers:
tee = '├── '
last = '└── '


class FileSystem(ABC):
    def __init__(self, **kwargs):
        self.__client__ = kwargs.get("client", None)

    @abstractmethod
    def lb(self):
        pass

    @abstractmethod
    def ls(self, path, recursive, grep=None):
        pass

    @abstractmethod
    def tree(self, path: Path, prefix: str = ''):
        pass

    @abstractmethod
    def stat(self, path: str):
        pass

    @abstractmethod
    def find(self, path: str, filename: str):
        pass

    @abstractmethod
    def read_bytes(self, filename: str):
        pass

    @abstractmethod
    def read_excel(self, filename: str):
        pass

    @abstractmethod
    def rm(self, paths: str):
        pass

    def grep(self, iterable: iter, regex: str) -> list:
        return [obj for obj in iterable if re.match(rf'{regex}', obj)]

    def cp(self, source, destination):
        """
        Copy a file from:
            1) Minio to local e.g cp("s3://bucket/folder/file.txt", "./file.txt")
            2) local to Minio e.g cp("./file.txt", "s3://bucket/folder/file.txt")
            3) local to local e.g cp("./file.txt", "./newfile/txt")
            4) Minio to minio e.g cp("s3://bucket/folder/file.txt", "s3://bucket/folder/newfile.txt")

        Prefix minio paths with a s3://
        """
        source_type = 'local'
        destination_type = 'local'
        if 's3://' in source:
            source_type = 'remote'
            source_path = source.split('s3://')[1]
            source_bucket, source_filename = self._process_path(source_path)
        if 's3://' in destination:
            destination_type = 'remote'
            destination_path = destination.split('s3://')[1]
            destination_bucket, destination_filename = self._process_path(destination_path)

        logger.info(f"Copying from {source_type}: {source} to {destination_type}: {destination}")

        if source_type == 'remote' and destination_type == 'local':
            self.__client__.fget_object(source_bucket, object_name=source_filename, file_path=destination)

        if source_type == 'local' and destination_type == 'remote':
            self.__client__.fput_object(destination_bucket, object_name=destination_filename, file_path=source)

        if source_type == 'local' and destination_type == 'local':
            shutil.copyfile(source, destination)

        if source_type == 'remote' and destination_type == 'remote':
            self.__client__.copy_object(destination_bucket, destination_filename,
                                        CopySource(source_bucket, source_filename))


class MinioFS(FileSystem):
    def __init__(self, hostname, access_key=None, secret_key=None, secure=True):
        client = Minio(hostname,
                       access_key=access_key,
                       secret_key=secret_key,
                       secure=secure)
        super().__init__(client=client)

    def lb(self, grep=None):
        """
        List all buckets.
        :return: list of tuples (name, creation date)
        """
        buckets = [bucket.name for bucket in self.__client__.list_buckets()]
        if grep:
            return self.grep(buckets, grep)
        else:
            return buckets

    def ls(self, path: str, recursive: bool = False, grep: str = None):
        """
        :param recursive:
        :param path: <bucket>/path/to/folder/in/bucket
        :param grep:
        :return:
        """
        bucket, prefix = self._process_path(path)
        objects = [obj.object_name for obj in self.__client__.list_objects(bucket,
                                                                           prefix=prefix,
                                                                           recursive=recursive)]
        if grep:
            return self.grep(objects, grep)
        else:
            return objects
        pass

    def tree(self, path: Path, prefix: str = ''):
        raise NotImplementedError("Tree list is not implemented for minio file system yet. Sorry ):")
        pass

    def stat(self, path):
        """

        :param path: path to directory or file. If directory, it will stat for all files in the directory.
        :return:
        """
        file_attributes = []
        bucket, prefix = self._process_path(path)
        for obj in self.__client__.list_objects(bucket, prefix=prefix, recursive=False):
            file_attributes.append({
                "name": obj.object_name,
                "type": "folder" if obj.is_dir else "file",
                "modified": datetime.strftime(obj.last_modified, "%Y-%m-%d %H:%M:%S"),
                "size": obj.size,
            })
        return file_attributes
        pass

    def find(self, path, filename):
        """
        Recursively look for a file starting from given path. Match exact, case sensitive.
        :param path: Starting directory to start looking top down
        :param filename: name of file to search for
        :return: path to file
        """
        filepaths = []
        bucket, prefix = self._process_path(path)
        for obj in self.__client__.list_objects(bucket, prefix=prefix, recursive=True):
            if filename in obj.object_name:
                filepaths.append(obj.object_name)

        return filepaths

    def read_bytes(self, filename):
        data = self._stream_file(filename)
        return b''.join(data)

    def read_excel(self, filename):
        """
        returns xlrd workbook object
        :param filename:
        :return: An instance of the :class:`~xlrd.book.Book` class.
        """
        data = self._stream_file(filename)
        return xlrd.open_workbook(file_contents=b''.join(data))

    def _process_path(self, path) -> (str, str):
        """
        Split path string into bucket and the prefix for usage in list_objects for the s3 api.
        :param path: Path in s3. Include bucket name in path.
        :return:
        """
        bucket = path.split('/')[0]
        prefix = '/'.join(path.split('/')[1:])
        return bucket, prefix

    def _stream_file(self, filename) -> list:
        data = []
        bucket, filepath = self._process_path(filename)
        file = self.__client__.get_object(bucket_name=bucket, object_name=filepath)
        for data_stream in file.stream(32 * 1024):
            data.append(data_stream)
        return data

    def query_csv(self, filename: str, sql: str):
        bucket, filepath = self._process_path(filename)
        data = self.__client__.select_object_content(bucket,
                                                     filepath,
                                                     SelectRequest(sql,
                                                                   CSVInputSerialization(file_header_info="USE"),
                                                                   CSVOutputSerialization(),
                                                                   request_progress=True)
                                                     )

        headers = self.__client__.select_object_content(bucket,
                                                        filepath,
                                                        SelectRequest("select * from s3object limit 1",
                                                                      CSVInputSerialization(file_header_info="NONE"),
                                                                      CSVOutputSerialization(),
                                                                      request_progress=True)
                                                        )
        bytearray = b""
        for line in headers.stream():
            bytearray = bytearray + line
        for line in data.stream():
            bytearray = bytearray + line
        return pd.read_csv(BytesIO(bytearray))

    def rm(self, paths):
        """
        :param paths:
        """
        if type(paths) != list:
            raise TypeError("Invalid type: paths is not a list.")
        filenames = set(map(lambda x: '/'.join(x.split('/')[1:]), paths))
        bucket_unique = set((map(lambda x: x.split('/')[0], paths)))
        if len(bucket_unique) != 1:
            raise ValueError(f"Removing files across multiple buckets ({bucket_unique}) is not permitted.")
        else:
            bucket = bucket_unique.pop()
        for filename in filenames:
            self.__client__.remove_object(bucket_name=bucket, object_name=filename)


class LocalFS(FileSystem):
    def lb(self, grep=None):
        """
        Since local fs has no such thing as buckets, we will just do a ls on the pwd.
        :param grep: regex pattern that will be matched using re.match()
        """
        return self.ls(path='.', grep=grep)

    def ls(self, path, recursive=False, grep=None):
        """
        :param path: path to list directory
        :param grep: regex pattern that will be matched using re.match()
        :return: list of files & folders in directory
        """
        if recursive:
            logger.warn("Recusrive mode only supported for minio file system. Will continue to run ls in non recursive"
                        "mode.")

        items = os.listdir(path)
        if grep:
            return self.grep(items, grep)
        else:
            return items

    def tree(self, path: Path, prefix: str = ''):
        """A recursive generator, given a directory Path object
        will yield a visual tree structure line by line
        with each line prefixed by the same characters

        example: fs.tree(Path()) to get tree for current working dir.
       for line in fs.tree(Path()):
            print(line)
        """
        contents = list(path.iterdir())
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():  # extend the prefix and recurse:
                extension = branch if pointer == tee else space
                # i.e. space because last, └── , above so no more |
                yield from self.tree(path, prefix=prefix + extension)

    def stat(self, path):
        """
        Get file statistics for files in the directory
        :param path: path to directory
        :return: list of file statistics
        """
        file_attributes = []

        if Path(path).is_dir():
            for file in Path(path).iterdir():
                stats = file.stat()
                file_attributes.append({
                    "name": file.name,
                    "type": "folder" if file.is_dir() else "file",
                    "modified": datetime.strftime(
                        datetime.fromtimestamp(stats.st_mtime, pytz.timezone("Asia/Singapore")), "%Y-%m-%d %H:%M:%S"),
                    "size": stats.st_size,
                })
        else:
            file = Path(path)
            stats = file.stat()
            file_attributes.append({
                "name": file.name,
                "type": "file",
                "modified": datetime.strftime(datetime.fromtimestamp(stats.st_mtime, pytz.timezone("Asia/Singapore")),
                                              "%Y-%m-%d %H:%M:%S"),
                "size": stats.st_size,
            })

        return file_attributes

    def find(self, path, filename):
        filepaths = []
        for root, dirs, files in os.walk(path):
            if filename in files:
                filepaths.append(os.path.join(root, filename))
        return filepaths

    def read_bytes(self, filename):
        """
        Read bytes of a file.
        :param filename: path to file to read.
        :return:
        """
        file = open(filename, "rb")
        return file.read()

    def read_excel(self, filename):
        """

        :param filename:
        :return: An instance of the :class:`~xlrd.book.Book` class.
        """
        return xlrd.open_workbook(filename)

    def rm(self, paths) -> None:
        if type(paths) != list:
            raise TypeError("Invalid type: paths is not a list.")
        for path in paths:
            logger.info(f"Removing file: {path}")
            os.remove(path)
        return

