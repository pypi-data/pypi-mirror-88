# miniMinio

A thin python helper get either 1) local files or 2) Minio objects. 1) Heavily relies on the default os library while 2) is built off [minio-py](https://github.com/minio/minio-py). The package is designed to provide a seamless switch between testing file operations locally/over a file system and interacting with a minio server when in deployment.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install miniMinio.

```bash
pip install miniMinio
```

## Quick Start

```python
from miniMinio import Minio

# For connecting to minio s3
mc = Minio(type="minio").config(hostname='host',
                                access_key='minio',
                                secret_key='minio',
                                secure=False
                                )
mc.ls('bucket/dir/')

# For connecting to local filesystem
mc = Minio(type="local").config()
mc.ls('.')
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/) 


