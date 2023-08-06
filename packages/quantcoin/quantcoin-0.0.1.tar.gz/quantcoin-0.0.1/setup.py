# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.rst") as f:
    readme = f.read()

setup(
    name="quantcoin",
    version="0.0.1",
    description="Package for backtesting and paper trading cryptocurrency.",
    long_description=readme,
    author="GetQuantCoin",
    author_email="tuan@quantcoin.co",
    url="https://github.com/GetQuantCoin/quantcoin",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "pandas",
        "backtesting",
        "ujson",
        "requests"
    ],
)