#!/usr/bin/env python

from setuptools import setup

from django_nlf import __version__ as dnlf_version


with open('README.md') as desc:
    LONG_DESCRIPTION = desc.read()

with open('requirements.txt') as reqs:
    REQUIREMENTS = reqs.readlines()

setup(
    name='django-nlf',
    version=dnlf_version,
    description='Django Natural Language Filter package',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Hodossy, Szabolcs',
    author_email='hodossy.szabolcs@gmail.com',
    maintainer='Hodossy, Szabolcs',
    maintainer_email='hodossy.szabolcs@gmail.com',
    url='https://github.com/hodossy/django-nlf',
    license='MIT',
    platforms='any',
    packages=['django_nlf'],
    keywords=['django', 'natural-Language', 'filtering'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Typing :: Typed',
    ],
    python_requires='>=3.7',
    install_requires=REQUIREMENTS,
)
