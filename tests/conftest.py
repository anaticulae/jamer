# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import jamer

# import jamer

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(jamer.ROOT)
