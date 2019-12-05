# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import jam.pdf
import tests.resources


def test_pdf_pagenumber():
    """Count number of pages of document."""
    pages = jam.pdf.pagenumber(tests.resources.MASTER_72PAGES)
    assert pages == 72


def test_pdf_remove():
    """Remove first 10 pages."""
    removed = jam.pdf.remove(tests.resources.MASTER_72PAGES, tuple(range(10)))
    pages = jam.pdf.pagenumber(removed)
    assert pages == 72 - 10


def test_pdf_select():
    """Select last three pages of document."""
    selected = jam.pdf.select(tests.resources.MASTER_72PAGES, (69, 70, 71))
    pages = jam.pdf.pagenumber(selected)
    assert pages == 3
