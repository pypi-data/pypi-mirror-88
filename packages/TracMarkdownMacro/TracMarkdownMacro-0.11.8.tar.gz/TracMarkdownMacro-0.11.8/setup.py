#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Douglas Clifton <dwclifton@gmail.com>
# Copyright (C) 2012-2013 Ryan J Ollos <ryan.j.ollos@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

import os.path
from setuptools import setup

setup(
    name='TracMarkdownMacro',
    packages=['Markdown'],
    version='0.11.8',

    author='Douglas Clifton',
    author_email='dwclifton@gmail.com',
    maintainer='Ryan J Ollos',
    maintainer_email='ryan.j.ollos@gmail.com',
    description='Implements Markdown syntax WikiProcessor as a Trac macro.',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    long_description_content_type='text/markdown',
    keywords='0.11 dwclifton processor macro wiki',
    url='https://trac-hacks.org/wiki/MarkdownMacro',
    license='BSD 3-Clause',

    entry_points={'trac.plugins': ['Markdown.macro = Markdown.macro']},
    classifiers=['Framework :: Trac'],
    install_requires=['Trac'],
)
