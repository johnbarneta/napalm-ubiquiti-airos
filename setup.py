from setuptools import setup, find_packages

__author__ = 'Juan Gomez <jgomez@phicus.es>'


with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_reqs(file_path):
    with open(file_path, 'rt') as fobj:
        lines = map(str.strip, fobj)
        lines = filter(None, lines)
        lines = filter(lambda x: x.startswith("#"), lines)
        return tuple(lines)


setup(
    name="napalm-ubiquiti-airos",
    version="0.0.1",
    packages=find_packages(),
    author="Juan Gomez",
    author_email="jgomez@phicus.es",
    description="Network Automation and Programmability Abstraction Layer driver for Ubiquti AirOS using SSH",
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    url="https://github.com/johnbarneta/napalm-ubiquiti-airos",
    include_package_data=True,
    install_requires=(
        'napalm==2.*',
        'netmiko==2.*',
    ),
)
