#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

from jamer.freestyle import write_blank_pdf
from jamer.pdf import hashcontent
from jamer.pdf import pagenumber
from jamer.pdf import remove
from jamer.pdf import select
from jamer.pdf import switch
from jamer.pdf import write
from jamer.script import run
from jamer.script import scriptfile

__version__ = importlib.metadata.version('jamer')

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROCESS = 'jamer'
