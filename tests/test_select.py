# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila

import jam
import tests.resources

SELECT = """
# select some text content of the first page and remove empty page

sel page_0.text_5_1360
"""


def test_script_select(testdir):
    script = os.path.join(testdir.tmpdir, 'source.py')
    utila.file_create(script, SELECT)
    outpath = os.path.join(testdir.tmpdir, 'output.pdf')
    assert jam.pagenumber(tests.resources.SCALED_PDF) == 2
    jam.run(
        script,
        document=tests.resources.SCALED_PDF,
        outpath=outpath,
    )
    assert jam.pagenumber(outpath) == 1
