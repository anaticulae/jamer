# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import utila
import utilatest

import jamer.cat

small = functools.partial(
    utilatest.run_cov,
    process='pdfcat',
    main=jamer.cat.main,
    expect=True,
)


def test_pdfcat(td, mp):
    source = power.MASTER116_PDF
    before = utila.file_size(source)
    outpath = td.tmpdir.join('small.pdf')
    small(cmd=f'-o {outpath} {source} 0:2', mp=mp)
    after = utila.file_size(outpath)
    assert after < before
