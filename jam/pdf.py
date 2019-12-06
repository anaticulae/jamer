# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib
import os

import PyPDF2
import utila

import jam


def pagenumber(path: str) -> int:
    assert os.path.isfile(path), str(path)
    loaded = PyPDF2.PdfFileReader(stream=open(path, mode='rb'))
    return loaded.getNumPages()


def remove(path, pages: tuple) -> str:
    assert os.path.isfile(path), str(path)
    numbers = pagenumber(path)
    hold = [item for item in range(numbers) if item not in pages]
    result = select(path, hold)
    return result


def select(path: str, pages: tuple) -> str:
    assert os.path.isfile(path), str(path)
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


def switch(path: str, pages: list) -> str:
    assert os.path.isfile(path), str(path)
    assert all([len(item) == 2 for item in pages]), 'require list of tuples'
    numbers = pagenumber(path)
    origin = list(range(numbers))
    for flip_a, flip_b in pages:
        origin[flip_a], origin[flip_b] = origin[flip_b], origin[flip_a]
    flipped = tuple(origin)
    outpath = select(path, flipped)
    return outpath


def hashcontent(path: str, pages=None) -> int:
    """Determine hash of textual content of document stored in `path`.

    Args:
        path(str): path to pdf file to run hash for.
        pages(list): selected pages to compute hash. If None all pages
                     are hashed.
    Returns:
        Common hash for selected content.
    """
    assert os.path.isfile(path), str(path)
    if isinstance(pages, int):
        pages = [pages]
    textcount = []
    with open(path, mode='rb') as source:
        reader = PyPDF2.PdfFileReader(stream=source)
        selected = range(reader.getNumPages()) if pages is None else pages
        for number in selected:
            page = reader.getPage(number)
            with contextlib.suppress(KeyError):
                textcontent = page['/Resources']['/Font']
                textcount.append(len(textcontent))
    return hash(str(textcount))
