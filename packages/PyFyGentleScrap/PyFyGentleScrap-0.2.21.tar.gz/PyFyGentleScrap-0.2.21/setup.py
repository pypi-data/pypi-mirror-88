# coding: utf-8
# !/usr/bin/python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyFyGentleScrap",
    version="0.2.21",
    author="OlivierLuG",
    author_email="not_a_valid_email@gmail.com",
    description="Unofficial Yahoo finance scrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://gitlab.com/OlivierLuG/pyfygentlescrap",
    packages=setuptools.find_packages(exclude=["pyfygentlescrap.tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        line.strip() for line in open("requirements.txt", "r").readlines()
    ],
)
