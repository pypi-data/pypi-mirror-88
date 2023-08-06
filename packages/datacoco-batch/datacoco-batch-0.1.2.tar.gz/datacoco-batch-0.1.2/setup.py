#!/usr/bin/env python

from setuptools import setup
setup(
    name="datacoco-batch",
    version="0.1.2",
    author="Equinox",
    description="Data common code for batch workflows by Equinox",
    long_description=open("README.rst").read(),
    url="https://github.com/equinoxfitness/datacoco-batch",
    keywords = ['helper', 'config', 'logging', 'common'],
    scripts=[],
    license="MIT",
    packages = ['datacoco_batch'],
    install_requires=["requests==2.*"]
)
