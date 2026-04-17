# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import jamer.cli
import jamer.pdf
import jamer.script

CMD = [
    utila.cli.Parameter(
        longcut='--remove',
        message='remove defined pages out of document',
    ),
    utila.cli.Parameter(
        longcut='--switch',
        message='switch pages with each other',
    ),
    utila.cli.Parameter(
        longcut='--script',
        message='run modification script on resource',
    ),
    utila.Flag(
        longcut='--printtext',
        message='run modification script on resource',
    ),
]


def work(inpath: str, outpath: str, pages, args: dict) -> int:
    result = utila.SUCCESS
    if args['printtext']:
        printtext(inpath, pages)
        return utila.SUCCESS
    if args['--remove']:
        result += remove(inpath, outpath, pages)
    if args['--switch']:
        result += switch(inpath, outpath, args['--switch'])
    if args['--script']:
        result += script(inpath, outpath, args['--script'])
    return result


def printtext(inpath: str, pages: tuple) -> int:  # pylint:disable=W0613
    document = jamer.script.Document(inpath)
    for page, content in document.pages().items():
        utila.log(page)
        utila.log('[')
        for item in content.text_stream():
            utila.log(f'({item[0]}, {item[1]}),', end=' ')
        utila.log('\n]')


def remove(source: str, sink: str, pages: tuple) -> int:
    utila.log(f'remove: {pages}\nfrom: {source}\nresult: {sink}')
    tmp = jamer.pdf.remove(source, pages)
    utila.copy_content(tmp, sink)
    utila.log('completed')
    return utila.SUCCESS


def switch(source: str, sink: str, selected: str) -> int:
    parsed = parse_switch(selected)
    if parsed is None:
        utila.error(f'invalid switch argument `{selected}`')
        return utila.INVALID_COMMAND

    switched = jamer.pdf.switch(source, parsed)
    utila.copy_content(switched, sink)
    utila.log('completed')
    return utila.SUCCESS


def script(source: str, sink: str, scriptpath: str) -> int:
    failure = jamer.script.run(script=scriptpath, document=source, outpath=sink)
    if failure:
        return failure
    utila.log('completed')
    return utila.SUCCESS


def parse_switch(raw) -> list:
    splitted = raw.split('|')
    result = []
    for item in splitted:
        try:
            left, right = item.split(',')
            left, right = int(left), int(right)
            result.append((left, right))
        except ValueError:
            return None
    return result
