#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="tap-twitter-ads",
    version="0.0.1",
    description="Singer.io tap for extracting data from the Twitter Ads API",
    author="Dreamdata",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_twitter_ads"],
    install_requires=["requests==2.20.0", "singer-python==5.9.0",],
    extras_require={"dev": ["ipdb"]},
    entry_points="""
      [console_scripts]
      tap-twitter-ads=tap_twitter_ads:main
    """,
    packages=find_packages(),
)
