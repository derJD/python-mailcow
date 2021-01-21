#!/usr/bin/env python

from os import getenv
from setuptools import setup, find_packages


def get_version(version="9999.999.99-dev9"):
    for env in ["CI_COMMIT_TAG", "VERSION"]:
        version = getenv(env, version)

    return version


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="python-mailcow",
    version=get_version(),
    author="Jean-Denis Gebhardt",
    author_email="projects@der-jd.de",
    description="Interact with mailcow API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com./derJD/python-mailcow",
    license="GPLv3+",
    package_dir={"": "src"},
    packages=find_packages("src/"),
    python_requires=">=3.6.0",
    install_requires=['requests', 'ptable', 'configparser'],
    entry_points={"console_scripts": ["mailcow = mailcow.cli:main"]},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
)
