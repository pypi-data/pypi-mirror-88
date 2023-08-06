# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
# type: ignore
import codecs
import os.path

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def parse_dependency(filepath):
    return [
        dependency
        for dependency in open(filepath).read().splitlines()
        if "==" in dependency
    ]


base_requirements = parse_dependency("requirements/base.txt")
dev_requirements = base_requirements + parse_dependency("requirements/dev.txt")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtenv",
    version=get_version("mtenv/__init__.py"),
    author="Shagun Sodhani, Ludovic Denoyer, Olivier Delalleau",
    author_email="sshagunsodhani@gmail.com, denoyer@fb.com, odelalleau@fb.com",
    description="MTEnv: Environment interface for mulit-task reinforcement learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=base_requirements,
    url="https://github.com/facbookresearch/mtenv",
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "docs", "docsrc"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        # Install development dependencies with
        # pip install -e .[dev]
        "dev": dev_requirements,
    },
)
