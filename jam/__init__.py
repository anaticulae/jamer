#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

from jam.freestyle import write_blank_pdf
from jam.pdf import hashcontent
from jam.pdf import pagenumber
from jam.pdf import remove
from jam.pdf import select
from jam.pdf import switch
from jam.pdf import write
from jam.script import run
from jam.script import scriptfile

__version__ = '0.2.17'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PACKAGE = 'jam'
