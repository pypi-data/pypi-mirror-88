# Abstract Factory
import datetime
import os
import time
from abc import ABC, abstractmethod

from minio import Minio

exclude = {".minio.sys"}


class ConnectionClient():
    def set_file_server_type(self, file_server):
        if file_server == "local":
            return LocalFactory()
        if file_server == "minio":
            return MinioFactory()
        raise TypeError("Unknown file server type")


class Product(ABC):
    @abstractmethod
    def create_connection(self, hostname, access_key, secret_key, secure):
        pass

    @abstractmethod
    def get_buckets(self, remote_dir):
        pass

    @abstractmethod
    def get_all_object_details_in_bucket(self, bucket_name=None, attributes=["object_name", "last_modified"],
                                         filter_object=("file", "folder")):
        pass

    @abstractmethod
    def get_object_details_in_bucket(self, object_name, bucket_name=None, attributes=["object_name", "last_modified"]):
        pass

    @abstractmethod
    def get_object_path(self, bucket_name, file_name):
        pass

    @abstractmethod
    def get_single_object_from_bucket_to_file(self, object_name, dir_path, bucket_name=None):
        pass

    @abstractmethod
    def get_single_object_content_bytes(self, object_name, bucket_name=None):
        pass

    @abstractmethod
    def get_single_excel_file_content(self, excel_file_object, bucket_name=None):
        pass

    @abstractmethod
    def get_single_csv_file_content(self, csv_file_object, bucket_name=None):
        pass

    @abstractmethod
    def upload_dataframe_to_csv(self, csv_file_object_name, df, bucket_name=None):
        pass


class LocalFactory(Product):
    def create_connection(self, hostname, access_key, secret_key, secure):
        return "local"

    def get_buckets(self, remote_dir):
        store = []
        remote_dir = os.getcwd()
        for dirpath, dirs, filenames in os.walk(remote_dir, topdown=True):
            dirs[:] = set(dirs) - exclude
            for f in filenames:
                if f[0] == ".":
                    continue
                else:
                    path = os.path.abspath(os.path.join(dirpath, f))
                    store.append((path, datetime.datetime.strptime(time.ctime(os.path.getctime(path)),
                                                                   "%a %b %d %H:%M:%S %Y")))


class MinioFactory(Product):
    def __init__(self):
        self.client = ''

    def create_connection(self, hostname, access_key, secret_key, secure):
        client = Minio(hostname, access_key, secret_key, secure)
        self.client = client

    def get_buckets(self, remote_dir):
        client = self.client
        store = []
        all_buckets = client.list_buckets()
        for bucket in all_buckets:
            store.append((bucket.name, bucket.creation_date))
        return store
