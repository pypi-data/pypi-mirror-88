#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='dict_cmp',
    version='0.0.2',
    author='oyj',
    author_email='wisecsj@gmail.com',
    url='',
    description=u'tesla dict校验库',
    packages= ["dict_cmp"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'jujube=jujube_pill:jujube',
            'pill=jujube_pill:pill'
        ]
    }
)