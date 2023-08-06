#!/usr/bin/env python

import os
import pprint
from setuptools import setup, find_namespace_packages

import logging

logger = logging.getLogger(__name__)

setup_requirements = ["pytest-runner", "setuptools_scm"]

version_file = "./VERSION"
readme_file = "./README.md"


def read_file(fname, strip=True):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    data = ""
    if os.path.exists(fn):
        with open(fn) as f:
            data = f.read()
            data = data.strip() if strip else data
            # logger.info(f"Got data '{data}' from '{fn}'")
    else:
        logger.error(f"Could not find file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return data


def remove_comment(line, sep="#"):
    i = line.find(sep)
    if i >= 0:
        line = line[:i]
    return line.strip()


def read_requirements_file(fname: str):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    print(f"Reading requirements from {fn}")
    lines = []
    if os.path.exists(fn):
        with open(fn) as f:
            for r in f.readlines():
                r = r.strip()
                if len(r) < 1:
                    continue
                r = remove_comment(r)
                if len(r) < 1:
                    continue
                lines.append(r)
    else:
        logger.error(f"Could not find requirements file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return lines


package = {
    "name": "octomy-common",
    "version": read_file(version_file),
    "author": "Lennart Rolland",
    "author_email": "lennart@octomy.org",
    "maintainer": "Lennart Rolland",
    "maintainer_email": "lennart@octomy.org",
    "description": ("OctoMY common"),
    "license": "GPL-3 LGPL-3 MIT",
    "platforms": ["Linux"],
    "keywords": "octomy common",
    "url": "https://gitlab.com/octomy/common",
    "packages": find_namespace_packages(include=['fk.*', ]),
    "zip_safe": True,
    "long_description": read_file(readme_file),
    "long_description_content_type": "text/markdown",
    "setup_requires": setup_requirements,
    "zip_safe": True,
    "install_requires": read_requirements_file("requirements/requirements.in"),  # Allow flexible deps for install
    "tests_require": read_requirements_file("requirements/test_requirements.txt"),  # Use rigid deps for testing
    "test_suite": "tests",
    "python_requires": ">=3.7.4",
    "data_files": [("common", [version_file])],
    "include_package_data": True,
    # From https://pypi.org/pypi?%3Aaction=list_classifiers
    "classifiers": ["Development Status :: 3 - Alpha", "Intended Audience :: Developers", "Intended Audience :: Other Audience", "Topic :: Utilities", "Natural Language :: English", "Operating System :: POSIX :: Linux", "Programming Language :: Python :: 3.7", "Topic :: Other/Nonlisted Topic"],
}

pprint.pprint(package)
setup(**package)
