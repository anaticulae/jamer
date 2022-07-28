# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import pdfsmall.optimize


@utilatest.nightly
def test_small(testdir):
    source = power.MASTER116_PDF
    before = utila.file_size(source)
    outpath = os.path.join(testdir.tmpdir, 'small.pdf')
    pdfsmall.optimize.small(source, outpath)
    after = utila.file_size(outpath)
    assert after < before


@utilatest.longrun
def test_ghost(testdir):
    source = power.MASTER116_PDF
    before = utila.file_size(source)
    outpath = os.path.join(testdir.tmpdir, 'small.pdf')
    pdfsmall.optimize.ghost_small(source, outpath)
    after = utila.file_size(outpath)
    assert after < before
