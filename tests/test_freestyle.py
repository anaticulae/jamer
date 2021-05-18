# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import jam


def test_write_blank_pages(testdir):
    destination = os.path.join(testdir.tmpdir, 'empty_pages.pdf')
    jam.write_blank_pdf(10, destination)

    assert jam.pagenumber(destination) == 10
