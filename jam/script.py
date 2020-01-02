# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""script
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

import PyPDF2
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

    script = scriptfile(script)
    try:
        # NOTE: USE IMPORT AGAIN AFTER FIXING/HAVING NEW PYLINT VERSION
        runpy = importlib.import_module('runpy')
        runpy.run_path(
            script,
            init_globals=environment,
            run_name=None,
        )
        jam.pdf.write(outpath, doc.loaded)
    except SyntaxError as error:
        utila.error(error)
        return utila.FAILURE
    return utila.SUCCESS if status.ready else utila.FAILURE


class Document:

    def __init__(self, source: str):
        assert os.path.isfile(source), str(source)
        self.loaded = PyPDF2.PdfFileReader(stream=open(source, mode='rb'))

    def pages(self):
        return {
            f'page_{number}': PageHook(self.loaded.getPage(number))
            for number in range(self.loaded.getNumPages())
        }


class PageHook:

    def __init__(self, page: PyPDF2.pdf.PageObject):
        self.page = page

    def __delattr__(self, name):
        pass


def scriptfile(path: str) -> str:
    """Create scriptfile for exection and surround code with error
    handler.

    Args:
        path(str): path to source code file
    Returns:
        Path to generated source code file which contains error handler.
    """
    loaded = utila.file_read(path)
    # ensure indent
    loaded = [f'    {item}' for item in loaded.splitlines()]
    loaded = utila.NEWLINE.join(loaded)
    with_final = (ERROR_HANDLER % loaded)

    filepath = utila.tmpfile(jam.ROOT)
    utila.file_replace(filepath, with_final)
    return filepath


ERROR_HANDLER = """\
try:
    %s
except Exception as error:
    print(error)
    __status.error = True
else:
    __status.ready = True
"""
