"""\
Concatenate pages from pdf files into a single pdf file.

Page ranges refer to the previously-named file.
A file not followed by a page range means all the pages of the file.

PAGE RANGES are like Python slices.
        {page_range_help}
EXAMPLES
    pdfcat -o output.pdf head.pdf content.pdf :6 7: tail.pdf -1
        Concatenate all of head.pdf, all but page seven of content.pdf,
        and the last page of tail.pdf, producing output.pdf.

    pdfcat chapter*.pdf >book.pdf
        You can specify the output file by redirection.

    pdfcat chapter?.pdf chapter10.pdf >book.pdf
        In case you don't want chapter 10 before chapter 2.
"""
# Copyright (c) 2014, Steve Witham <switham_github@mac-guyver.com>.
# All rights reserved. This software is available under a BSD license;
# see https://github.com/mstamy2/PyPDF2/LICENSE

import argparse
import os
import sys
import traceback

from PyPDF2 import PdfMerger
from PyPDF2 import parse_filename_page_ranges
from PyPDF2.pagerange import PageRange


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__.format(page_range_help=PageRange.__init__.__doc__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="output_file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show page ranges as they are being read",
    )
    parser.add_argument(
        "first_filename",
        nargs=1,
        metavar="filename [page range...]",
    )
    # argparse chokes on page ranges like "-2:" unless caught like this:
    parser.add_argument(
        "fn_pgrgs",
        nargs=argparse.REMAINDER,
        metavar="filenames and/or page ranges",
    )
    args = parser.parse_args()
    args.fn_pgrgs.insert(0, args.first_filename[0])
    return args


def main():
    args = parse_args()
    filename_page_ranges = parse_filename_page_ranges(args.fn_pgrgs)
    if args.output:
        output = open(args.output, "wb")  # pylint:disable=R1732
    else:
        sys.stdout.flush()
        output = os.fdopen(sys.stdout.fileno(), "wb")
    merger = PdfMerger()
    in_fs = dict()
    try:
        for (filename, page_range) in filename_page_ranges:
            if args.verbose:
                print(filename, page_range, file=sys.stderr)
            if filename not in in_fs:
                in_fs[filename] = open(filename, "rb")  # pylint:disable=R1732
            merger.append(in_fs[filename], pages=page_range)
    except Exception:  # pylint:disable=broad-except
        print(traceback.format_exc(), file=sys.stderr)
        print("Error while reading " + filename, file=sys.stderr)
        sys.exit(1)
    merger.write(output)
    # In 3.0, input files must stay open until output is written.
    # Not closing the in_fs because this script exits now.
    sys.exit(0)
