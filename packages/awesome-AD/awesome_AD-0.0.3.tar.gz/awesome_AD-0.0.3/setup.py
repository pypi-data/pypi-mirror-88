#!/usr/bin/env python
# coding=utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awesome_AD",
    version="0.0.3",
    author="Berry12kiwi (ac207 Group 8): Xingyu Liu, Sarah Zeng, Qinyi Chen",
    author_email="charlotteliu12x@gmail.com, Sarah_zeng@college.Harvard.edu, qychen@seas.harvard.edu",
    description="A package of automatic differentiation with both Forward Mode and Reserve Mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berry12kiwi/cs107-FinalProject/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    install_requires=['numpy>=1.16.3',
                      'pandas>=0.23.4',
                      'networkx>=2.2',
                      'pytest>=2.7.2',
                      'matplotlib>=3.0.2',
                      ]
)
