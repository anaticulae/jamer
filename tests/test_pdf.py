# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import jam.pdf


def test_pdf_pagenumber():
    """Count number of pages of document."""
    pages = jam.pdf.pagenumber(power.MASTER072_PDF)
    assert pages == 72


def test_pdf_remove():
    """Remove first 10 pages."""
    removed = jam.pdf.remove(power.MASTER072_PDF, tuple(range(10)))
    pages = jam.pdf.pagenumber(removed)
    assert pages == 72 - 10


def test_pdf_select():
    """Select last three pages of document."""
    selected = jam.pdf.select(power.MASTER072_PDF, (69, 70, 71))
    pages = jam.pdf.pagenumber(selected)
    assert pages == 3


def test_pdf_switch():
    """Switch list of pages with each other"""
    flip = [(1, 2), (3, 4), (6, 5), (20, 60)]
    switched = jam.pdf.switch(power.MASTER072_PDF, pages=flip)
    pages = jam.pdf.pagenumber(switched)
    assert pages == 72

    before = jam.pdf.hashcontent(power.MASTER072_PDF)
    after = jam.pdf.hashcontent(switched)
    assert after != before


def test_pdf_switch_empty():
    flip = []
    switched = jam.pdf.switch(power.MASTER072_PDF, pages=flip)

    before = jam.pdf.hashcontent(power.MASTER072_PDF)
    after = jam.pdf.hashcontent(switched)
    # No flip, origin must have the same content as not flipped result
    assert after == before
