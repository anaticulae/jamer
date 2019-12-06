# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import jam.cli
import jam.pdf

CMD = [
    utila.cli.Parameter(
        longcut='--remove',
        message='remove defined pages out of document',
    ),
]


def work(inpath: str, outpath: str, pages, args: dict) -> int:
    if args['--remove']:
        remove(inpath, outpath, pages)
    return utila.SUCCESS


def remove(source: str, sink: str, pages: tuple):
    utila.log(f'remove: {pages}\nfrom: {source}\nresult: {sink}')
    tmp = jam.pdf.remove(source, pages)
    utila.copy_content(tmp, sink)
    utila.log('completed')
