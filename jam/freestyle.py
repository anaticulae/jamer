# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import PyPDF2


def write_blank_pdf(
    numbers: int,
    path: str,
    width: float = 768,
    height: float = 1024,
):
    """Create a pdf file which contains white, blank pages only."""
    assert numbers >= 1, str(numbers)
    writer = PyPDF2.PdfFileWriter()
    for _ in range(numbers):
        writer.insertBlankPage(width=width, height=height)
    with open(path, 'wb') as sink:
        writer.write(sink)
