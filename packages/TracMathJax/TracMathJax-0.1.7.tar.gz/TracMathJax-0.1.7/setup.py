#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011-2024 Mitar <mitar.trac@tnode.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from setuptools import setup

VERSION = '0.1.7'
PACKAGE = 'mathjax'

setup(
    name='TracMathJax',
    version=VERSION,
    description="Renders mathematical equations using MathJax library.",
    author='Mitar',
    author_email='mitar.trac@tnode.com',
    url='https://trac-hacks.org/wiki/TracMathJaxPlugin',
    keywords='trac plugin',
    license="AGPLv3",
    classifiers=['Framework :: Trac'],
    packages=[PACKAGE],
    include_package_data=True,
    package_data={
        PACKAGE: ['htdocs/*.js'],
    },
    install_requires=[],
    zip_safe=False,
    entry_points={
        'trac.plugins': '%s = %s.api' % (PACKAGE, PACKAGE),
    },
)
