#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements


install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]


def read(file_name):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    :param file_name: Name of the file.
    :return: The text of the file.
    """
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name="nlp-parsers",
    version="0.1.0",
    author="ryan-panos",
    author_email="randompkp@yahoo.com",
    description=("nlp-parsers"),
    license="Monitor 360 owns code",
    url="https://github.com/ryan-panos/nlp-parsers.git",
    # packages=find_packages(exclude=['test']),
    install_requires=reqs,
    # long_description=read(file_name='README.md'),
)
