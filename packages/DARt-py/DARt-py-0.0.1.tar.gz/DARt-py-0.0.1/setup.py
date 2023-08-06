#!/usr/bin/env python
# coding: utf-8

import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="DARt-py",
    version="0.0.1",
    author="Xian Yang, Shuo Wang, Yuting Xing, Ling Li, Richard Yi Da Xu, Karl J.Friston and Yike Guo",
    author_email="y.xing19@imperial.ac.uk",
    description="A tool to estimate Instantaneous Reproduction Number(Rt) for the pandemic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kerr93/DARt/tree/master/DARt",
    packages=setuptools.find_packages(),
    install_requires=['numpy','scipy.stats','random','pandas','tqdm','math'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    #python_requires='>=3.6',
)