# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Script
======

The script environment enables the possiblity to modify a pdf file.

example
-------

.. code-block:: python

    page_0.text_0 = 'hello world'

    page_0.text_5.size = 14
    page_0.text_5.font = 'Verdana'

    page_0.text_3.bold = True

    del page_0.text_1

.. note::

    Importing `runpy` leads to internal pylint error.

    Solution: use importlib
"""
import dataclasses
import importlib
import os
import re

import PyPDF2
import PyPDF2._utils
import PyPDF2.constants
import PyPDF2.generic
import utila

import jam
import jam.pdf


@dataclasses.dataclass
class Status:
    ready: bool = False
    error: bool = False


def run(script: str, document: str, outpath: str) -> int:
    doc = Document(document)
    status = Status()
    environment = {'__status': status}
    environment.update(doc.pages())
    environment.update({'pages': doc.pagenumbers()})

    script = scriptfile(script)
    try:
        # NOTE: USE IMPORT AGAIN AFTER FIXING/HAVING NEW PYLINT VERSION
        runpy = importlib.import_module('runpy')
        runpy.run_path(
            script,
            init_globals=environment,
            run_name=None,
        )
        jam.pdf.write(outpath, doc.loaded, remove_empty=True)
    except SyntaxError as error:
        utila.error(error)
        return utila.FAILURE
    return utila.SUCCESS if status.ready else utila.FAILURE


class Document:

    def __init__(self, source: str):
        assert os.path.isfile(source), str(source)
        self.loaded = PyPDF2.PdfReader(stream=open(source, mode='rb'))  # pylint:disable=R1732

    def pages(self) -> dict:
        result = {
            f'page_{number}': PageHook(self.loaded._get_page(number))  # pylint:disable=W0212
            for number in range(self.loaded._get_num_pages())  # pylint:disable=W0212
        }
        return result

    def pagenumbers(self) -> list:
        return list(range(self.loaded._get_num_pages()))  # pylint:disable=W0212


class PageHook:

    def __init__(self, page: PyPDF2.PageObject):
        self.page = page

    def __delattr__(self, name):
        pass

    def text_stream(self):
        ContentStream = PyPDF2.generic.ContentStream
        content = self.page["/Contents"].get_object()
        if not isinstance(content, ContentStream):
            content = ContentStream(content, self.page.pdf)
        # Note: we check all strings are TextStringObjects.  ByteStringObjects
        # are strings where the byte->string encoding was unknown, so adding
        # them to the text here would be gibberish.
        separator = []
        start = None
        for index, (_, operator) in enumerate(content.operations):
            if operator == PyPDF2._utils.b_("BT"):  # pylint:disable=W0212
                start = index
            elif operator == PyPDF2._utils.b_("ET"):  # pylint:disable=W0212
                separator.append((start, index))
        return separator

    def shrink_stream(self, todo: list):
        ContentStream = PyPDF2.generic.ContentStream
        content = self.page["/Contents"].get_object()
        if not isinstance(content, ContentStream):
            content = ContentStream(content, self.page.pdf)
        result = []
        for start, end in todo:
            result.extend(content.operations[start:end + 1])
        content.operations = result
        self.page.__setitem__(
            PyPDF2.generic.NameObject('/Contents'),
            content,
        )
        self.page.compress_content_streams()


def scriptfile(path: str) -> str:
    """Create scriptfile for execution and surround code with error
    handler.

    Args:
        path(str): path to source code file
    Returns:
        Path to generated source code file which contains error handler.
    """
    loaded = utila.file_read(path)
    # ensure indent
    loaded = [
        f'    {prepare(item)}' for item in loaded.splitlines() if item.strip()
    ]
    loaded = utila.NEWLINE.join(loaded)
    program = PROGRAM % loaded
    with_final = (ERROR_HANDLER % program)

    filepath = utila.tmpfile(jam.ROOT)
    utila.file_replace(filepath, with_final)
    return filepath


SELECT_TEXTLINE = r'^sel page_(?P<page>\d+)\.text_(?P<start>\d+)_(?P<end>\d+)$'


def prepare(line) -> str:
    """\
    >>> prepare('sel page_0.text_0_10')
    'SELECTED_TEXT[0].append((0,10))'
    """
    line = line.strip()
    if line.startswith('print('):
        return line
    if line.startswith('assert'):
        return line
    matched = re.match(SELECT_TEXTLINE, line)
    if matched:
        return f'SELECTED_TEXT[{matched["page"]}].append(({matched["start"]},{matched["end"]}))'
    if line.startswith('#'):
        # comment
        return line
    return f'# NOT SUPPORTED: {line}'


PROGRAM = """\
    import collections
    SELECTED_TEXT = collections.defaultdict(list)
%s
    if SELECTED_TEXT:
        # remove others
        for page in pages:
            current = globals()[f'page_{page}']
            current.shrink_stream(SELECTED_TEXT[page])
"""

ERROR_HANDLER = """\
import utila
try:
%s
except Exception:
    utila.log_stacktrace()
    __status.error = True
else:
    __status.ready = True
"""
