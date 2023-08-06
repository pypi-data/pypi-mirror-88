import os

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    readme = f.read()

setup_args = {
    "name": "ueca",
    "version": "0.1.0",
    "description": "基礎化学実験AのためのPythonライブラリ",
    "long_description": readme,
    "long_description_content_type": "text/markdown",
    "license": "MIT License",
    "author": "puman03(Aki)",
    "author_email": "a03ki04@gmail.com",
    "url": "https://github.com/A03ki/ueca",
    "python_requires": ">=3.6, <3.9",
    "install_requires": ["numpy", "pint", "scipy", "sympy", "uncertainties"],
    "extras_require": {"tests": ["pytest"]},
    "packages": find_packages(),
    "include_package_data": True,
    "classifiers": [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    "keywords": "UEC"
}

setup(**setup_args)
