# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
    pagenumbers: int = None
    with open(path, mode='rb') as pdf:
        loaded = PyPDF2.PdfReader(stream=pdf)
        pagenumbers = loaded._get_num_pages()  # pylint:disable=W0212
    return pagenumbers


def remove(path, pages: tuple) -> str:
    assert os.path.isfile(path), str(path)
    numbers = pagenumber(path)
    hold = [item for item in range(numbers) if item not in pages]
    result = select(path, hold)
    return result


def select(path: str, pages: tuple) -> str:
    assert os.path.isfile(path), str(path)
    writer = PyPDF2.PdfWriter()
    with open(path, mode='rb') as source:
        reader = PyPDF2.PdfReader(stream=source)
        for number in pages:
            page = reader._get_page(number)  # pylint:disable=W0212
            writer.add_page(page)
        outpath = utila.tmpfile(jam.ROOT)
        with open(outpath, 'wb') as sink:
            writer.write(sink)
    return outpath


def switch(path: str, pages: list = None) -> str:
    assert os.path.isfile(path), str(path)
    if not pages:
        pages = []
    assert all(len(item) == 2 for item in pages), 'require list of tuples'
    numbers = pagenumber(path)
    origin = list(range(numbers))
    for flip_a, flip_b in pages:
        origin[flip_a], origin[flip_b] = origin[flip_b], origin[flip_a]
    flipped = tuple(origin)
    outpath = select(path, flipped)
    return outpath


def write(path: str, source, remove_empty: bool = False):
    writer = PyPDF2.PdfWriter()
    for number in range(source._get_num_pages()):  # pylint:disable=W0212
        page = source._get_page(number)  # pylint:disable=W0212
        if remove_empty and not page.extract_text().strip():
            # skip empty page
            continue
        writer.add_page(page)
    with open(path, 'wb') as sink:
        writer.write(sink)


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
        reader = PyPDF2.PdfReader(stream=source)
        selected = range(reader._get_num_pages()) if pages is None else pages  # pylint:disable=W0212
        for number in selected:
            page = reader._get_page(number)  # pylint:disable=W0212
            with contextlib.suppress(KeyError):
                textcontent = page['/Resources']['/Font']
                textcount.append(len(textcontent))
    return hash(str(textcount))
