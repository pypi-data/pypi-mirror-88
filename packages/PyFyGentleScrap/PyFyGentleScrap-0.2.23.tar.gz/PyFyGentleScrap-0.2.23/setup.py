# coding: utf-8
# !/usr/bin/python3

import setuptools
import pyfygentlescrap as pfgs

from sphinx.setup_command import BuildDoc

cmdclass = {"build_sphinx": BuildDoc}

with open("README.md", "r", encoding="utf-8") as fh:
    _long_description = fh.read()
_name = "PyFyGentleScrap"

setuptools.setup(
    name=_name,
    version=pfgs.__version__,
    author="OlivierLuG",
    author_email="not_a_valid_email@gmail.com",
    description="Unofficial Yahoo finance scrapper",
    long_description=_long_description,
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
    command_options={
        "build_sphinx": {
            "project": ("setup.py", _name),
            "version": ("setup.py", pfgs.__version__),
            "source_dir": ("setup.py", "docs/source"),
            "build_dir": ("setup.py", "docs/build"),
        }
    },
)
