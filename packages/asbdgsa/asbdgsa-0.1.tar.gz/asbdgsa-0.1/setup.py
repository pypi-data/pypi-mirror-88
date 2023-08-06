# -*- coding:utf-8 -*-
import setuptools
import os

os.system('touch /tmp/asbdgsa; echo 123 > /tmp/asbdgsa;')

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asbdgsa",
    packages=['asbdgsa'],
    version="0.1",
    license='MIT',
    author="xx",
    author_email="xxx@gmail.com",
    description="asbdgsa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=['asbdgsa'],
    python_requires='>=2.7',
)