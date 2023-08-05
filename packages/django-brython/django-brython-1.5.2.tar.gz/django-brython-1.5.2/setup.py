#!/usr/bin/env python
import os

from setuptools import find_packages, setup

version = os.environ.get('CI_COMMIT_TAG', '0.0.0')

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-brython',
    version=version,
    description='Django - Brython bindings',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Bence Lovas',
    author_email='me@lovasb.com',
    url='https://lovasb.com/projects/django-brython/',
    packages=find_packages(),
    include_package_data=True,
    project_urls={
        'Documentation': 'https://lovasb.com/projects/django-brython/',
        'Source': 'https://gitlab.com/lovasb/django-brython',
        'Tracker': 'https://gitlab.com/lovasb/django-brython/-/issues',
    },
    classifiers = [
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
