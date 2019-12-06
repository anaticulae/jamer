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
    ['-i', 'filedoesnotexists'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove', '0:X'],
    ['-i', tests.resources.MASTER_72PAGES, '--remove', '1000'],
])
@pytest.mark.usefixtures('testdir')
def test_run_external_failure(cmd, monkeypatch):
    tests.run_failure(cmd, monkeypatch=monkeypatch)


def test_run_remove(testdir, monkeypatch):
    root = str(testdir)

    cmd = ['-i', tests.resources.MASTER_72PAGES, '--remove', '0:10']
    tests.run_success(cmd, monkeypatch=monkeypatch)

    _, name = os.path.split(tests.resources.MASTER_72PAGES)
    outpath = os.path.join(root, name)
    assert os.path.exists(outpath), str(outpath)

    pagenumbers = jam.pdf.pagenumber(outpath)
    assert pagenumbers == 62
