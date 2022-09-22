# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import utila
import utilatest

import pdfsmall.cli
import pdfsmall.optimize

small = functools.partial(
    utilatest.run_cov,
    process='pdfsmall',
    main=pdfsmall.cli.main,
    expect=True,
)


@utilatest.nightly
def test_small(td, mp):
    source = power.MASTER116_PDF
    before = utila.file_size(source)
    outpath = td.tmpdir.join('small.pdf')
    small(cmd=f'-i {source} -o {outpath}', mp=mp)
    after = utila.file_size(outpath)
    assert after < before


@utilatest.longrun
def test_ghost(td):
    source = power.MASTER116_PDF
    before = utila.file_size(source)
    outpath = td.tmpdir.join('small.pdf')
    pdfsmall.optimize.ghost_small(source, outpath)
    after = utila.file_size(outpath)
    assert after < before
