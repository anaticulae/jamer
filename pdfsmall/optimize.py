# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import PyPDF2
import utila


def small(source: str, destination: str):
    writer = PyPDF2.PdfFileWriter()
    with open(source, mode='rb') as stream, open(destination, 'wb') as sink:
        reader = PyPDF2.PdfFileReader(stream=stream)
        # compress data stream
        for number in range(reader.getNumPages()):
            page = reader.getPage(number)
            page.compressContentStreams()
            writer.addPage(page)
        writer.removeImages()
        writer.write(sink)


GHOST = 'gswin64c' if os.name == 'nt' else 'gs'


def ghost_small(source: str, destination: str):
    config = '-sDEVICE=pdfwrite -dBATCH -dNOPAUSE -SAFE'
    cmd = f'{GHOST} {config} -sOutputFile={destination} {source}'
    utila.run(cmd)
