__author__ = 'pmagdon'
import os
from setuptools import setup, find_packages
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "FEPY",
    version = "0.0.1",
    author = "Paul Magdon",
    author_email = "pmagdon@gwdg.de",
    description = ("An programm to process RapidEye satellite images"),
    license = "BSD",
    keywords = "Remote Sensing, Image Processing",
    url = "http://134.76.194.191/wordpress/",
    packages=find_packages(),
    #install_requires = ['gdal>=1.11','lxml','datetime','rasterio'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)