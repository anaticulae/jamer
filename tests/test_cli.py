# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest

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
    ['-i', tests.resources.MASTER, '--remove', '1'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove', '0:X'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove', '1000'],
    ['-i', tests.resources.MASTER_72PAGES, '--switch', 'notasplit'],
])
@pytest.mark.usefixtures('testdir')
def test_run_external_failure(cmd, monkeypatch):
    tests.run_failure(cmd, monkeypatch=monkeypatch)


def test_run_non_existing_output(testdir, monkeypatch):
    root = str(testdir)
    outpath = os.path.join(root, 'abc/dfc')
    cmd = f'-i {tests.resources.MASTER_72PAGES} -o {outpath} --remove 1'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    outpath = os.path.join(root, 'abc/output.pdf')
    cmd = f'-i {tests.resources.MASTER_72PAGES} -o {outpath} --remove 1'
    tests.run_success(cmd, monkeypatch=monkeypatch)


def test_run_remove(testdir, monkeypatch):
    root = str(testdir)

    cmd = ['-i', tests.resources.MASTER_72PAGES, '--remove', '0:10']
    tests.run_success(cmd, monkeypatch=monkeypatch)

    _, name = os.path.split(tests.resources.MASTER_72PAGES)
    outpath = os.path.join(root, name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 62


@pytest.mark.parametrize('raw, before, after', [
    ('0,1|10,20', [0, 1, 10, 20], [1, 0, 20, 10]),
    ('10,20', [10, 20], [20, 10]),
])
def test_run_switch(testdir, monkeypatch, raw, before, after):
    root = str(testdir)

    cmd = ['-i', tests.resources.MASTER_72PAGES, '--switch', raw]
    tests.run_success(cmd, monkeypatch=monkeypatch)

    _, name = os.path.split(tests.resources.MASTER_72PAGES)
    outpath = os.path.join(root, name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 72

    hashed = jam.pdf.hashcontent(tests.resources.MASTER_72PAGES, before)

    # ensure that page flip does work
    after_hashed = jam.pdf.hashcontent(outpath, after)
    assert after_hashed == hashed, 'switch does not work'

    after_hashed = jam.pdf.hashcontent(outpath, before)
    assert after_hashed != hashed


def test_run_remove_to_output(testdir, monkeypatch):
    root = str(testdir)
    outpath = os.path.join(root, 'removed.pdf')

    cmd = f'-i {tests.resources.MASTER_72PAGES} -o {outpath} --remove 0:10'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    assert os.path.exists(outpath), str(outpath)
    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 62
