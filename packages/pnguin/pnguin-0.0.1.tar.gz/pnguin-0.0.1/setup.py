"""setup file for pnguin deployments
"""

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pnguin",
    version="0.0.1",
    description="A simple, dual-axis DataFrame library with remote support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raghavmecheri/pnguin",
    author="Raghav Mecheri",
    author_email="raghav.mecheri@columia.edu",
    license="MIT",
    download_url="https://github.com/raghavmecheri/pnguin/archive/0.0.1.zip",
    packages=["pnguin"],
    install_requires=["numpy==1.19.4", "pydantic==1.7.3", "tabulate==0.8.7"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.7",
    ],
)
