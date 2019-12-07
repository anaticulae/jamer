# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import jam

RESOURCES = os.path.join(jam.ROOT, 'tests/resources')

MASTER = os.path.join(RESOURCES, 'master')
MASTER_72PAGES = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

EXAMPLE = os.path.join(jam.ROOT, 'tests/example')
HELLO_WORLD = os.path.join(EXAMPLE, 'helloworld.py')

REQUIRED_RESOURCES = [
    MASTER_72PAGES,
    HELLO_WORLD,
]
