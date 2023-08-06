from setuptools import setup, find_packages

with open('VERSION.txt', 'r') as v:
    version = v.read().strip()

with open('README.md', 'r') as r:
    readme = r.read()

download_url = (
    'https://github.com/jerinpetergeorge/python-json-logger/tarball/%s'
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="redis-json-logger",
    version=version,
    author="Jerin Peter George",
    author_email="jerinpetergeorge@gmail.com",
    description="An extension of Python's built-in logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jerinpetergeorge/python-json-logger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    download_url=download_url % version,
    install_requires=['redis'],
    license='MIT-Zero'
)
