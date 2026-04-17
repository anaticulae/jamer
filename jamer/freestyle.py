# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import PyPDF2

PAGE_COUNT_MAX = 100000


def write_blank_pdf(
    numbers: int,
    path: str,
    width: float = 768,
    height: float = 1024,
):
    """Create a pdf file which contains white, blank pages only."""
    assert numbers >= 1, str(numbers)
    assert numbers <= PAGE_COUNT_MAX, f'too many pages: {numbers} <= {PAGE_COUNT_MAX}'
    with open(path, 'wb') as sink:
        with PyPDF2.PdfWriter(fileobj=sink) as writer:
            for _ in range(numbers):
                writer.add_blank_page(
                    width=width,
                    height=height,
                )
