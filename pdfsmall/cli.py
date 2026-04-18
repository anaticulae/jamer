# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import sys

import utilo
import utilo.cli

import pdfsmall
import pdfsmall.optimize


@utilo.saveme
def main():
    # evaluate cli
    inpath, outpath = inout()
    # run ghost script
    pdfsmall.optimize.ghost_small(inpath, outpath)
    utilo.log(f'done: {outpath}')
    sys.exit(utilo.SUCCESS)


HEADER = b'%PDF-1.'


def ispdf(path: str) -> bool:
    """\
    >>> ispdf(__file__)
    False

    TODO: REPLACE WITH PDFINFO
    """
    try:
        header = utilo.file_read_binary(path, size=len(HEADER))
    except PermissionError:
        return False
    if not header == HEADER:
        return False
    return True


def inout():
    parser = utilo.cli.create_parser(
        todo=[],
        config=utilo.ParserConfiguration(
            cacheflag=False,
            inputparameter=True,
            multiprocessed=False,
            outputparameter=True,
            pages=False,
            prefix=False,
            singleinput=True,
            waitingflag=False,
        ),
        version=pdfsmall.__version__,
    )
    args = utilo.parse(parser)
    inpath, outpath = utilo.sources(args, singleinput=True)  # pylint:disable=W0632
    inpath = inpath[0]
    if not ispdf(inpath):
        utilo.error(f'require single pdf file: {inpath}')
        sys.exit(utilo.FAILURE)
    name = f'{utilo.file_name(inpath)}_opt.pdf'
    outpath = os.path.join(outpath, name)
    return inpath, outpath
