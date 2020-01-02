#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
        pages=False,
    )
    args = utila.parse(parser)
    inpath, outpath = determine_inputoutput(args)
    validated = validate_resources(inpath, args)
    if validated:
        return validated

    if os.path.isdir(outpath):
        _, name = os.path.split(inpath)
        outpath = os.path.join(outpath, name)

    pages = extract_pages(args)
    if pages:
        pages = parse_pages(pages)

    result = jam.cli.operation.work(inpath, outpath, pages, args)
    return result


def determine_inputoutput(args: dict):
    # support single input and output file
    outpath = args['output']
    if outpath and outpath.endswith('.pdf'):
        # single output file
        del args['output']
        inpath, _ = utila.sources(args, singleinput=True)
    else:
        inpath, outpath = utila.sources(args, singleinput=True)
    # support only one input
    inpath = inpath[0] if isinstance(inpath, list) else inpath
    return inpath, outpath


def validate_resources(inpath: str, args: dict):
    pages = extract_pages(args)
    if not os.path.isfile(inpath):
        utila.error(f'require valid pdf file as input, got: {inpath}')
        return utila.INVALID_COMMAND
    if pages:
        if not PyPDF2.PageRange.valid(pages):
            utila.error(f'invalid --pages `{pages}` parameter')
            return utila.INVALID_COMMAND
        pages = parse_pages(pages)
        if not valid_range(inpath, pages):
            utila.error(f'--pages `{pages}` out of range')
            return utila.INVALID_COMMAND
    return utila.SUCCESS


def extract_pages(args):
    if args['--remove']:
        return args['--remove']
    return None


def valid_range(path: str, pages: tuple):
    ranged = jam.pdf.pagenumber(path)
    valid = set(range(ranged))
    return all([item in valid for item in pages])


def parse_pages(pages: str):
    ranged = PyPDF2.PageRange(pages)
    sliced = ranged.to_slice()
    return tuple(range(sliced.start, sliced.stop))
