# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilatest

import jam


def test_write_blank_pages(td):
    destination = td.tmpdir.join('empty_pages.pdf')
    jam.write_blank_pdf(10, destination)
    assert jam.pagenumber(destination) == 10


@pytest.mark.timeout(120)
@utilatest.nightly
def test_write_blank_verylong(td):
    destination = td.tmpdir.join('verylong.pdf')
    pagecount = 10000
    jam.write_blank_pdf(pagecount, destination)
    assert jam.pagenumber(destination) == pagecount
