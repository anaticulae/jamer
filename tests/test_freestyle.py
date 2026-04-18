# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilotest

import jamer


def test_write_blank_pages(td):
    destination = td.tmpdir.join('empty_pages.pdf')
    jamer.write_blank_pdf(10, destination)
    assert jamer.pagenumber(destination) == 10


@pytest.mark.timeout(120)
@utilotest.nightly
def test_write_blank_verylong(td):
    destination = td.tmpdir.join('verylong.pdf')
    pagecount = 10000
    jamer.write_blank_pdf(pagecount, destination)
    assert jamer.pagenumber(destination) == pagecount
