# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import PyPDF2
import utila

import jam


def pagenumber(path: str) -> int:
    loaded = PyPDF2.PdfFileReader(stream=open(path, mode='rb'))
    return loaded.getNumPages()


def remove(path, pages: tuple) -> str:
    numbers = pagenumber(path)
    hold = [item for item in range(numbers) if item not in pages]
    result = select(path, hold)
    return result


def select(path: str, pages: tuple) -> str:
    writer = PyPDF2.PdfFileWriter()
    with open(path, mode='rb') as source:
        reader = PyPDF2.PdfFileReader(stream=source)
        for number in pages:
            page = reader.getPage(number)
            writer.addPage(page)
        outpath = utila.tmpfile(jam.ROOT)
        with open(outpath, 'wb') as sink:
            writer.write(sink)
    return outpath
