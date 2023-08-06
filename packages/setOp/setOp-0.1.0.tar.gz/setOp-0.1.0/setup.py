#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup

setup(
    name='setOp',
    version='0.1.0',
    author='wws',
    author_email='onewesong@gmail.com',
    url='https://github.com/onewesong/setOp',
    description=u'Compared files with through python set operations.',
    packages=['setop'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'setop=setop:main',
        ]
    }
)
