# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import utilatest

import jam
import tests
import tests.resources


@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['--version'],
])
@pytest.mark.usefixtures('testdir')
def test_run_external(cmd, monkeypatch):
    tests.run_success(cmd, monkeypatch=monkeypatch)


@pytest.mark.parametrize('cmd', [
    ['-i', 'filedoesnotexists.pdf'],
    ['-i', power.RESOURCES, '--remove', '1'],
    ['-i', power.MASTER072_PDF, '--remove'],
    ['-i', power.MASTER072_PDF, '--remove', '0:X'],
    ['-i', power.MASTER072_PDF, '--remove', '1000'],
    ['-i', power.MASTER072_PDF, '--switch', 'notasplit'],
])
@pytest.mark.usefixtures('testdir')
def test_run_external_failure(cmd, monkeypatch):
    tests.run_failure(cmd, monkeypatch=monkeypatch)


def test_run_non_existing_output(testdir, monkeypatch):
    outpath = os.path.join(testdir.tmpdir, 'abc/dfc')
    cmd = f'-i {power.MASTER072_PDF} -o {outpath} --remove 1'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    outpath = os.path.join(testdir.tmpdir, 'abc/output.pdf')
    cmd = f'-i {power.MASTER072_PDF} -o {outpath} --remove 1'
    tests.run_success(cmd, monkeypatch=monkeypatch)


def test_run_remove(testdir, monkeypatch):
    cmd = ['-i', power.MASTER072_PDF, '--remove', '0:10']
    tests.run_success(cmd, monkeypatch=monkeypatch)

    _, name = os.path.split(power.MASTER072_PDF)
    outpath = os.path.join(testdir.tmpdir, name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 62


@pytest.mark.parametrize('raw, before, after', [
    ('0,1|10,20', [0, 1, 10, 20], [1, 0, 20, 10]),
    ('10,20', [10, 20], [20, 10]),
])
def test_run_switch(testdir, monkeypatch, raw, before, after):
    cmd = ['-i', power.MASTER072_PDF, '--switch', raw]
    tests.run_success(cmd, monkeypatch=monkeypatch)

    _, name = os.path.split(power.MASTER072_PDF)
    outpath = os.path.join(testdir.tmpdir, name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 72

    hashed = jam.pdf.hashcontent(power.MASTER072_PDF, before)

    # ensure that page flip does work
    after_hashed = jam.pdf.hashcontent(outpath, after)
    assert after_hashed == hashed, 'switch does not work'

    after_hashed = jam.pdf.hashcontent(outpath, before)
    assert after_hashed != hashed


def test_run_remove_to_output(testdir, monkeypatch):
    outpath = os.path.join(testdir.tmpdir, 'removed.pdf')

    cmd = f'-i {power.MASTER072_PDF} -o {outpath} --remove 0:10'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    assert os.path.exists(outpath), str(outpath)
    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 62


def test_run_script(testdir, monkeypatch, capsys):
    outpath = os.path.join(testdir.tmpdir, 'abc.pdf')

    cmd = (f'-i {power.MASTER072_PDF} -o {outpath} '
           f'--script {tests.resources.HELLO_WORLD}')
    tests.run_success(cmd, monkeypatch=monkeypatch)

    stdout = utilatest.stdout(capsys)
    assert 'hello world' in stdout

    assert os.path.exists(outpath), str(outpath)


def test_printtext(testdir, monkeypatch, capsys):
    source = tests.resources.SCALED_PDF
    cmd = f'-i {source} --printtext'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    stdout = utilatest.stdout(capsys)
    assert 'page_0' in stdout
    assert 'page_1' in stdout
    assert 'page_2' not in stdout
