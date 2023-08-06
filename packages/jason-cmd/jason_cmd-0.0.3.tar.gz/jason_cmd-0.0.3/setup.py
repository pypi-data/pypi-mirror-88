#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jason_cmd", # Replace with your own username
    version="0.0.3",
    author="ilpg ",
    author_email="chrismdjr@gmail.com",
    description="Shell command manager and flag handler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ilpg/jason",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# Make the dist files: python3 setup.py sdist bdist_wheel
# Upload them: python3 -m twine upload --repository pypi dist/*
