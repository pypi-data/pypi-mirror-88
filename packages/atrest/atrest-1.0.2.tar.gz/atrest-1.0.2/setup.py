from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README-pypi.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="atrest",
    version="1.0.2",
    author="Jonathan Weaver",
    author_email="createchange@protonmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Basic Autotask REST Client",
    packages=find_packages(exclude=["test"]),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
