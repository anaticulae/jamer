# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import jamer

RESOURCES = utilo.join(jamer.ROOT, 'tests/resources', exist=True)

SCALED_PDF = utilo.join(RESOURCES, 'scaled.pdf', exist=True)

EXAMPLE = utilo.join(jamer.ROOT, 'tests/example', exist=True)
HELLO_WORLD = utilo.join(EXAMPLE, 'helloworld.py', exist=True)

SCRIPT_SIMPLE_DELETE = utilo.join(EXAMPLE, 'simpledelete.pys', exist=True)
SCRIPT_SIMPLE_CHANGE = utilo.join(EXAMPLE, 'simplechange.pys', exist=True)
SCRIPT_SIMPLE_SELECT = utilo.join(EXAMPLE, 'simpleselect.pys', exist=True)

REQUIRED_RESOURCES = [
    HELLO_WORLD,
    SCRIPT_SIMPLE_CHANGE,
    SCRIPT_SIMPLE_DELETE,
    SCRIPT_SIMPLE_SELECT,
    SCALED_PDF,
]
