from miniMinio.FileSystem import MinioFS, LocalFS


class Minio:
    def __init__(self, type):
        self.type = type
        pass

    def config(self, **kwargs):
        if self.type.lower() == 'minio':
            return MinioFS(**kwargs)
        elif self.type.lower() == 'local':
            return LocalFS(**kwargs)
        else:
            raise ValueError("Only Minio or Local Filesystem type allowed.")