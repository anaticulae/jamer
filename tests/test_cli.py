# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import pytest
import utilotest

import jamer
import tests
import tests.resources


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['--version'],
])
@pytest.mark.usefixtures('td')
def test_run_external(cmd, mp):
    tests.run(cmd, mp=mp)


@pytest.mark.parametrize('cmd', [
    ['-i', 'filedoesnotexists.pdf'],
    ['-i', hoverpower.RESOURCES, '--remove', '1'],
    ['-i', hoverpower.MASTER072_PDF, '--remove'],
    ['-i', hoverpower.MASTER072_PDF, '--remove', '0:X'],
    ['-i', hoverpower.MASTER072_PDF, '--remove', '1000'],
    ['-i', hoverpower.MASTER072_PDF, '--switch', 'notasplit'],
])
@pytest.mark.usefixtures('td')
def test_run_external_failure(cmd, mp):
    tests.fail(cmd, mp=mp)


def test_run_non_existing_output(td, mp):
    outpath = td.tmpdir.join('abc/dfc')
    cmd = f'-i {hoverpower.MASTER072_PDF} -o {outpath} --remove 1'
    tests.run(cmd, mp=mp)

    outpath = td.tmpdir.join('abc/output.pdf')
    cmd = f'-i {hoverpower.MASTER072_PDF} -o {outpath} --remove 1'
    tests.run(cmd, mp=mp)


def test_run_remove(td, mp):
    cmd = ['-i', hoverpower.MASTER072_PDF, '--remove', '0:10']
    tests.run(cmd, mp=mp)

    _, name = os.path.split(hoverpower.MASTER072_PDF)
    outpath = td.tmpdir.join(name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jamer.pdf.pagenumber(outpath)
    assert pagenumbers == 62


@pytest.mark.parametrize('raw, before, after', [
    ('0,1|10,20', [0, 1, 10, 20], [1, 0, 20, 10]),
    ('10,20', [10, 20], [20, 10]),
])
def test_run_switch(td, mp, raw, before, after):
    cmd = ['-i', hoverpower.MASTER072_PDF, '--switch', raw]
    tests.run(cmd, mp=mp)

    _, name = os.path.split(hoverpower.MASTER072_PDF)
    outpath = td.tmpdir.join(name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jamer.pdf.pagenumber(outpath)
    assert pagenumbers == 72

    hashed = jamer.pdf.hashcontent(hoverpower.MASTER072_PDF, before)

    # ensure that page flip does work
    after_hashed = jamer.pdf.hashcontent(outpath, after)
    assert after_hashed == hashed, 'switch does not work'

    after_hashed = jamer.pdf.hashcontent(outpath, before)
    assert after_hashed != hashed


def test_run_remove_to_output(td, mp):
    outpath = td.tmpdir.join('removed.pdf')

    cmd = f'-i {hoverpower.MASTER072_PDF} -o {outpath} --remove 0:10'
    tests.run(cmd, mp=mp)

    assert os.path.exists(outpath), str(outpath)
    pagenumbers = jamer.pdf.pagenumber(outpath)
    assert pagenumbers == 62


@utilotest.longrun
def test_run_script(td, mp, capsys):
    outpath = td.tmpdir.join('abc.pdf')

    cmd = (f'-i {hoverpower.MASTER072_PDF} -o {outpath} '
           f'--script {tests.resources.HELLO_WORLD}')
    tests.run(cmd, mp=mp)

    stdout = utilotest.stdout(capsys)
    assert 'hello world' in stdout

    assert os.path.exists(outpath), str(outpath)


def test_printtext(td, mp, capsys):  # pylint:disable=W0613
    source = tests.resources.SCALED_PDF
    cmd = f'-i {source} --printtext'
    tests.run(cmd, mp=mp)

    stdout = utilotest.stdout(capsys)
    assert 'page_0' in stdout
    assert 'page_1' in stdout
    assert 'page_2' not in stdout
