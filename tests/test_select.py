# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import jamer
import tests.resources

SELECT = """
# select some text content of the first page and remove empty page

sel page_0.text_5_1360
"""


def test_script_select(td):
    script = td.tmpdir.join('source.py')
    utilo.file_create(script, SELECT)
    outpath = td.tmpdir.join('output.pdf')
    assert jamer.pagenumber(tests.resources.SCALED_PDF) == 2
    jamer.run(
        script,
        document=tests.resources.SCALED_PDF,
        outpath=outpath,
    )
    assert jamer.pagenumber(outpath) == 1
