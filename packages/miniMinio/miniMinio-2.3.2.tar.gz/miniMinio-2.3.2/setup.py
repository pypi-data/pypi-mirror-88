import os
import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="miniMinio",
    version="2.3.2",
    author="Fruitjeus",
    author_email="jeu1993@gmail.com",
    description="Exposing file sharing system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        "minio==7.0.0",
        "loguru==0.3.2",
        "xlrd==1.2.0",
        "pytz==2020.4",
        "pandas==1.1.0"
    ],
    setup_requires=[
        "minio==7.0.0",
        "loguru==0.3.2",
        "xlrd==1.2.0",
        "pytz==2020.4",
        "pandas==1.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.1',
)
