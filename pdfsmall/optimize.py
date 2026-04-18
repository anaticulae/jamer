# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import PyPDF2
import utilo


def small(source: str, destination: str):
    writer = PyPDF2.PdfWriter()
    with open(source, mode='rb') as stream, open(destination, 'wb') as sink:
        reader = PyPDF2.PdfReader(stream=stream)
        # compress data stream
        for number in range(reader._get_num_pages()):  # pylint:disable=W0212
            page = reader._get_page(number)  # pylint:disable=W0212
            page.compress_content_streams()
            writer.add_page(page)
        writer.remove_images()
        writer.write(sink)


GHOST = 'gswin64c' if os.name == 'nt' else 'gs'


def ghost_small(source: str, destination: str):
    config = '-sDEVICE=pdfwrite -dBATCH -dNOPAUSE -SAFE'
    cmd = f'{GHOST} {config} -sOutputFile={destination} {source}'
    utilo.run(cmd)
