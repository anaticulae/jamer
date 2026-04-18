#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import PyPDF2
import utilo
import utilo.cli

import jamer
import jamer.cli.operation
import jamer.pdf


@utilo.saveme
def main():
    cmds = list(jamer.cli.operation.CMD)
    parser = utilo.cli.create_parser(
        todo=cmds,
        config=utilo.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
            pages=False,
            prefix=False,
        ),
        version=jamer.__version__,
    )
    args = utilo.parse(parser)
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

    result = jamer.cli.operation.work(inpath, outpath, pages, args)
    return result


def determine_inputoutput(args: dict):
    # support single input and output file
    outpath = args['output']
    if outpath and outpath.endswith('.pdf'):
        # single output file
        del args['output']
        inpath, _ = utilo.sources(args, singleinput=True)  # pylint:disable=W0632
    else:
        inpath, outpath = utilo.sources(args, singleinput=True)  # pylint:disable=W0632
    # support only one input
    inpath = inpath[0] if isinstance(inpath, list) else inpath
    return inpath, outpath


def validate_resources(inpath: str, args: dict):
    pages = extract_pages(args)
    if not os.path.isfile(inpath):
        utilo.error(f'require valid pdf file as input, got: {inpath}')
        return utilo.INVALID_COMMAND
    if pages:
        if not PyPDF2.PageRange.valid(pages):
            utilo.error(f'invalid --pages `{pages}` parameter')
            return utilo.INVALID_COMMAND
        pages = parse_pages(pages)
        if not valid_range(inpath, pages):
            utilo.error(f'--pages `{pages}` out of range')
            return utilo.INVALID_COMMAND
    return utilo.SUCCESS


def extract_pages(args):
    if args['--remove']:
        return args['--remove']
    return None


def valid_range(path: str, pages: tuple):
    ranged = jamer.pdf.pagenumber(path)
    valid = set(range(ranged))
    return all(item in valid for item in pages)


def parse_pages(pages: str):
    ranged = PyPDF2.PageRange(pages)
    sliced = ranged.to_slice()
    return tuple(range(sliced.start, sliced.stop))
