import pathlib
from setuptools import setup

# The text of the README file
with open("README.md", "r") as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="dontimport",
    version="1.0.0",
    description="Don't import this package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuperMaZingCoder/dontimport",
    author="SuperMaZingCoder",
    author_email="supermazingcoder@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["dontimport"],
)

