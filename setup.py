#!/usr/bin/env python3
"""
Setup script for KodeKloud Computer Quest.
"""

from setuptools import setup, find_packages

setup(
    name="computerquest",
    version="1.0.0",
    description="KodeKloud Computer Quest - An educational game about computer architecture",
    author="KodeKloud",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "computerquest=computerquest.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
    ],
)