#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='tesla_lib',
    version='0.0.3',
    author='oyj',
    author_email='wisecsj@gmail.com',
    url='',
    description=u'tesla dict校验库',
    packages= ["tesla_lib"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=jujube_pill:jujube',
            'pill=jujube_pill:pill'
        ]
    }
)