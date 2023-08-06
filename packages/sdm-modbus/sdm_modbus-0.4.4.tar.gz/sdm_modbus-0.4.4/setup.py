#!/usr/bin/env python3

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sdm_modbus",
    version="0.4.4",
    description="Eastron SDM Modbus parser library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="nmakel",
    author_email="",
    url="https://github.com/nmakel/sdm_modbus",
    packages=["sdm_modbus"],
    include_package_data=True,
    install_requires=[
        "pymodbus>=2.3.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ]
)
