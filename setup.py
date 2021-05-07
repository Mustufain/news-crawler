#!/usr/bin/python
import os

from setuptools import setup, find_packages

SRC_DIR = os.path.dirname(__file__)
CHANGES_FILE = os.path.join(SRC_DIR, "CHANGES")

with open(CHANGES_FILE) as fil:
    VERSION = fil.readline().split()[0]


setup(
    name="news_crawler",
    provides=["news_crawler"],
    description="crawls news articles and meta data",
    version=VERSION,
    packages=find_packages(exclude=['test']),
    author="abbasmustufain@gmail.com",
    entry_points={'console_scripts': [
        'news_crawler = news_crawler:main']},
    include_package_data=True
)
