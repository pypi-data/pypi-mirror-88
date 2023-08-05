#!/usr/bin/env python
import os

from setuptools import find_packages, setup

version = os.environ.get('CI_COMMIT_TAG', '0.0.0')

setup(
    name='django-brython',
    version=version,
    description='Django - Brython bindings',
    author='Bence Lovas',
    author_email='me@lovasb.com',
    url='https://lovasb.com',
    packages=find_packages(),
    include_package_data=True,

)
