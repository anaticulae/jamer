#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(ROOT, 'README.md'), encoding='utf8') as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'jam/__init__.py'), encoding='utf8') as fp:
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), encoding='utf8') as fp:
    REQUIRES = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    setuptools.setup(
        author='Helmut Konrad Schewe',
        author_email='info@checkitweg.de',
        description='modify test data',
        install_requires=REQUIRES,
        long_description=README,
        name='jam',
        platforms='any',
        url='https://dev.package.checkitweg.de/jam',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'jam',
            'jam.cli',
            'pdfsmall',
        ],
        entry_points={
            'console_scripts': [
                'jam = jam.cli:main',
                'pdfcat = jam.cat:main',
                'pdfsmall = pdfsmall.cli:main',
            ],
        },
    )
