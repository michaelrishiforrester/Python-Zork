#!/usr/bin/env python3
"""
Setup script for KodeKloud Computer Quest.

An educational text-based adventure game that teaches computer architecture concepts.
"""

import os
from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read version from the package
import re
with open(os.path.join("computerquest", "__init__.py"), encoding="utf-8") as f:
    version = re.search(r'__version__ = [\'"]([^\'"]*)[\'"]', f.read()).group(1)

setup(
    name="computerquest",
    version=version,
    description="KodeKloud Computer Quest - An educational game about computer architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="KodeKloud",
    author_email="info@kodekloud.com",
    url="https://github.com/kodekloud/computer-quest",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "computerquest=computerquest.main:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "pylint>=2.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Games/Entertainment",
    ],
    keywords="education, game, computer-architecture, text-adventure",
)