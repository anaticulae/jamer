# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# import power

# import jamer.pdf

# def test_pdf_pagenumber():
#     """Count number of pages of document."""
#     pages = jamer.pdf.pagenumber(power.MASTER072_PDF)
#     assert pages == 72

# def test_pdf_remove():
#     """Remove first 10 pages."""
#     removed = jamer.pdf.remove(power.MASTER072_PDF, tuple(range(10)))
#     pages = jamer.pdf.pagenumber(removed)
#     assert pages == 72 - 10

# def test_pdf_select():
#     """Select last three pages of document."""
#     selected = jamer.pdf.select(power.MASTER072_PDF, (69, 70, 71))
#     pages = jamer.pdf.pagenumber(selected)
#     assert pages == 3

# def test_pdf_switch():
#     """Switch list of pages with each other"""
#     flip = [(1, 2), (3, 4), (6, 5), (20, 60)]
#     switched = jamer.pdf.switch(power.MASTER072_PDF, pages=flip)
#     pages = jamer.pdf.pagenumber(switched)
#     assert pages == 72

#     before = jamer.pdf.hashcontent(power.MASTER072_PDF)
#     after = jamer.pdf.hashcontent(switched)
#     assert after != before

# def test_pdf_switch_empty():
#     switched = jamer.pdf.switch(power.MASTER072_PDF)
#     before = jamer.pdf.hashcontent(power.MASTER072_PDF)
#     after = jamer.pdf.hashcontent(switched)
#     # No flip, origin must have the same content as not flipped result
#     assert after == before
