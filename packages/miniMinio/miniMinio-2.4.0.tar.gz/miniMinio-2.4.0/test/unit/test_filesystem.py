from datetime import datetime
from unittest.mock import MagicMock
import pandas as pd
import pytest

from unittest import mock

import miniMinio


@pytest.fixture
@mock.patch('miniMinio.FileSystem.Minio')
def MinioFileSystem(Minio):
    fs = miniMinio.Minio(type='minio').config(**{
        "hostname": "test",
        "access_key": "test",
        "secret_key": "test",
        "secure": False
    })
    return fs


@pytest.fixture
def LocalFileSystem():
    return miniMinio.Minio(type='local').config()


def test_minio_lb(MinioFileSystem):
    """
    list buckets should be called once and return a list of tuples (name, creation_date)
    """
    bucket = MagicMock()
    bucket.name = 'test'
    bucket.creation_date = '2020-01-01'
    MinioFileSystem.__client__.list_buckets.return_value.__iter__.return_value = [bucket]
    output = MinioFileSystem.lb()
    MinioFileSystem.__client__.list_buckets.assert_called_once()
    assert output == [bucket.name]


def test_minio_ls(MinioFileSystem):
    object = MagicMock()
    object.object_name = 'test'
    MinioFileSystem.__client__.list_objects.return_value.__iter__.return_value = [object]
    output = MinioFileSystem.ls('bucket/filepath/test.txt')
    MinioFileSystem.__client__.list_objects.assert_called_once_with('bucket',
                                                                    prefix='filepath/test.txt',
                                                                    recursive=False)
    assert output == [object.object_name]


def test_minio_tree(MinioFileSystem):
    with pytest.raises(NotImplementedError):
        MinioFileSystem.tree('test')


def test_minio_stat(MinioFileSystem):
    object = MagicMock()
    object.object_name = 'test'
    object.is_dir = True
    object.last_modified = datetime(2020, 1, 1, 0, 0, 0)
    object.size = 1234
    MinioFileSystem.__client__.list_objects.return_value.__iter__.return_value = [object]
    output = MinioFileSystem.stat('bucket/testpath')
    MinioFileSystem.__client__.list_objects.assert_called_once_with('bucket', prefix='testpath', recursive=False)

    assert output == [{
        "name": "test",
        "type": "folder",
        "modified": "2020-01-01 00:00:00",
        "size": 1234
    }]


def test_minio_find(MinioFileSystem):
    object = MagicMock()
    object.object_name = 'test/filename.csv'
    MinioFileSystem.__client__.list_objects.return_value.__iter__.return_value = [object]
    output = MinioFileSystem.find('bucket/test/', 'filename.csv')
    MinioFileSystem.__client__.list_objects.assert_called_once_with('bucket', prefix='test/', recursive=True)
    assert output == ["test/filename.csv"]


@mock.patch('miniMinio.FileSystem.MinioFS._stream_file')
def test_minio_read_bytes(stream_file, MinioFileSystem):
    stream_file.return_value = [b'some', b'data', b'to', b'test']
    output = MinioFileSystem.read_bytes("bucket/test.txt")
    stream_file.assert_called_once_with("bucket/test.txt")
    assert output == b'somedatatotest'


@mock.patch('miniMinio.FileSystem.xlrd.open_workbook')
@mock.patch('miniMinio.FileSystem.MinioFS._stream_file')
def test_minio_read_excel(stream_file, open_workbook, MinioFileSystem):
    stream_file.return_value = [b'some', b'data', b'to', b'test']
    MinioFileSystem.read_excel('bucket/somefile.xls')
    stream_file.assert_called_once_with("bucket/somefile.xls")
    open_workbook.assert_called_once_with(file_contents=b'somedatatotest')


def test_minio_process_path(MinioFileSystem):
    bucket, prefix = MinioFileSystem._process_path('bucket/the/path/to/some/file.txt')
    assert bucket == 'bucket'
    assert prefix == 'the/path/to/some/file.txt'


def test_minio_stream_file(MinioFileSystem):
    file = MagicMock()
    file.stream.return_value = [b'some', b'bytes']
    MinioFileSystem.__client__.get_object.return_value=file

    output = MinioFileSystem._stream_file("bucket/file.txt")

    MinioFileSystem.__client__.get_object.assert_called_once_with(bucket_name="bucket", object_name="file.txt")
    assert output == [b'some', b'bytes']


def test_minio_rm(MinioFileSystem):
    MinioFileSystem.rm(["bucket/file1.txt", "bucket/file2.txt"])
    assert MinioFileSystem.__client__.remove_object.call_count == 2


@mock.patch('miniMinio.FileSystem.LocalFS.ls')
def test_local_lb(ls, LocalFileSystem):
    LocalFileSystem.lb()
    ls.assert_called_once_with(path='.', grep=None)


@mock.patch('miniMinio.FileSystem.os.listdir')
def test_local_ls(listdir, LocalFileSystem):
    LocalFileSystem.ls(path='.')
    listdir.assert_called_once_with('.')


@mock.patch('miniMinio.FileSystem.Path.iterdir')
def test_local_stat_dir(iterdir, LocalFileSystem):
    stats = MagicMock()
    stats.st_mtime = 123456789
    stats.st_size = 123

    file = MagicMock()
    file.name = 'file.txt'
    file.stat.return_value = stats
    file.is_dir.return_value = False
    iterdir.return_value = [file]
    attributes = LocalFileSystem.stat('.')
    iterdir.assert_called_once()
    assert attributes == [{"name": "file.txt",
                          "type": "file",
                          "modified": '1973-11-30 05:03:09',
                          "size": 123}]


@mock.patch('miniMinio.FileSystem.Path')
def test_local_stat_file(Path, LocalFileSystem):
    stat = MagicMock()
    stat.st_mtime = 123456789
    stat.st_size = 123

    file = MagicMock()
    file.stat.return_value = stat
    file.name = 'text.txt'
    Path.return_value = file
    Path('./text.txt').is_dir.return_value = False

    attributes = LocalFileSystem.stat('./text.txt')
    assert attributes == [{"name": "text.txt",
                           "type": "file",
                           "modified": '1973-11-30 05:03:09',
                           "size": 123}]


@mock.patch('miniMinio.FileSystem.os.walk')
def test_local_find(walk, LocalFileSystem):
    walk.return_value = [('.', ('dir',), ('file.txt',))]
    paths = LocalFileSystem.find('.', 'file.txt')
    assert paths == ["./file.txt"]


@mock.patch('os.remove')
def test_local_rm(remove, LocalFileSystem):
    LocalFileSystem.rm(['./file1.txt', './file2.txt'])
    assert remove.call_count == 2


@pytest.mark.parametrize('destination', ['s3://bucket/text_destination.txt', './text_destination.txt'])
@pytest.mark.parametrize('source', ['s3://bucket/text_source.txt', './text_source.txt'])
@mock.patch('miniMinio.FileSystem.shutil.copyfile')
@mock.patch('miniMinio.FileSystem.CopySource')
def test_cp(copysource, copyfile, MinioFileSystem, destination, source):
    MinioFileSystem.cp(source=source, destination=destination)
    if source == 's3://text_source.txt' and destination == './text_destination.txt':
        MinioFileSystem.__client.__fget_object.assert_called_once_with('bucket',
                                                                       object_name='bucket/text_source.txt',
                                                                       file_path='./text_destination.txt')
        MinioFileSystem.__client__.fput_object.assert_not_called()
        MinioFileSystem.__cluent__.copy_object.assert_not_called()
        copyfile.assert_not_called()

    if source == './text_source.txt' and destination == 's3://bucket/text_destination.txt':
        MinioFileSystem.__client__.fput_object.assert_called_once_with('bucket',
                                                                       object_name='text_destination.txt',
                                                                       file_path='./text_source.txt')
        MinioFileSystem.__client__.fget_object.assert_not_called()
        MinioFileSystem.__client__.copy_object.assert_not_called()
        copyfile.assert_not_called()

    if source == './text_source.txt' and destination == './text_destination.txt':
        copyfile.assert_called_once_with(source, destination)
        MinioFileSystem.__client__.fget_object.assert_not_called()
        MinioFileSystem.__client__.copy_object.assert_not_called()
        MinioFileSystem.__client__.fput_object.assert_not_called()

    if source == 's3://bucket/text_source.txt' and destination == 's3://bucket/text_destination.txt':
        MinioFileSystem.__client__.copy_object.assert_called_once_with('bucket', 'text_destination.txt', copysource('bucket', 'text_source.txt'))
        MinioFileSystem.__client__.fget_object.assert_not_called()
        copyfile.assert_not_called()
        MinioFileSystem.__client__.fput_object.assert_not_called()


@mock.patch('miniMinio.FileSystem.BytesIO')
def test_minio_write_csv(bytesio, MinioFileSystem):
    df = MagicMock()
    csv_data = MagicMock()
    csv_bytes = [1, 2, 3, 4]
    csv_data.encode.return_value = csv_bytes
    df.to_csv.return_value = csv_data
    data = [1, 2, 3]
    bytesio.return_value = data
    MinioFileSystem.write_csv(df, 'bucket/folder/df.csv')
    MinioFileSystem.__client__.put_object.assert_called_once_with('bucket', 'folder/df.csv', data=data,
                                                                   length=len(csv_bytes), content_type='application/csv')


def test_local_write_csv(LocalFileSystem):
    df = MagicMock()
    LocalFileSystem.write_csv(df, 'bucket/folder/df.csv')
    df.to_csv.assert_called_once_with('bucket/folder/df.csv', index=None, header=None)
