#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ibl-pipeline-light',
    version='0.1.0',
    description='Light version of ibl pipelineto access data in IBL database',
    author='Vathes',
    author_email='support@vathes.com',
    packages=find_packages(exclude=[]),
    install_requires=['datajoint>=0.12'],
)
