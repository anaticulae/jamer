#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import os

import PyPDF2
import utila
import utila.cli

import jam
import jam.cli.operation
import jam.pdf


@utila.saveme
def main():
    commands = []
    commands.extend(jam.cli.operation.CMD)

    parser = utila.cli.create_parser(
        commands,
        version=jam.__version__,
        outputparameter=True,
        inputparameter=True,
        prefix=False,
        pages=True,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True)
    if isinstance(inpath, list):
        inpath = inpath[0]

    validated = validate_resources(inpath, outpath, pages=args['pages'])
    if validated:
        return validated

    if os.path.isdir(outpath):
        _, name = os.path.split(inpath)
        outpath = os.path.join(outpath, name)

    pages = parse_pages(args['pages'])
    result = jam.cli.operation.work(inpath, outpath, pages, args)
    return result


def validate_resources(inpath: str, outpath: str, pages: str):
    if not inpath or not os.path.isfile(inpath) or not inpath.endswith('.pdf'):
        utila.error(f'require valid inpath, got: {inpath}')
        return utila.INVALID_COMMAND
    if not outpath.endswith('.pdf') and not os.path.exists(outpath):
        # check that directory to write exists
        utila.error(f'outpath does not exists: {outpath}')
        return utila.INVALID_COMMAND
    if pages is None:
        utila.error('require --pages parameter')
        return utila.INVALID_COMMAND
    if not PyPDF2.PageRange.valid(pages):
        utila.error(f'invalid --pages `{pages}` parameter')
        return utila.INVALID_COMMAND
    pages = parse_pages(pages)
    if not valid_range(inpath, pages):
        utila.error(f'--pages `{pages}` out of range')
        return utila.INVALID_COMMAND
    return utila.SUCCESS


def valid_range(path: str, pages: tuple):
    ranged = jam.pdf.pagenumber(path)
    valid = set(range(ranged))
    return all([item in valid for item in pages])


def parse_pages(pages: str):
    ranged = PyPDF2.PageRange(pages)
    sliced = ranged.to_slice()
    return tuple(range(sliced.start, sliced.stop))
