# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import jam.script
import tests.resources

EXAMPLE = """
print('hello')
page_0 = 5
"""

SYNTAX_ERROR = """
print('hello') 4
"""

RUNTIME_ERROR = """
assert 0
"""

MASTER = """
page_0.text_0 = 'hello world'

page_0.text_5.size = 14
page_0.text_5.font = 'Verdana'

page_0.text_3.bold = True

del page_0.text_1
"""


@pytest.mark.xfail(reason='not fully implemented')
def test_script_master(testdir):
    root = str(testdir)
    script = os.path.join(root, 'master.py')
    utila.file_create(script, MASTER)

    outpath = os.path.join(root, 'output.pdf')

    completed = jam.script.run(
        script,
        document=tests.resources.MASTER_72PAGES,
        outpath=outpath,
    )
    assert completed == utila.SUCCESS
    assert os.path.exists(outpath), str(outpath)


@pytest.mark.parametrize('code, expected', [
    pytest.param(EXAMPLE, utila.SUCCESS, id='simple'),
    pytest.param(SYNTAX_ERROR, utila.FAILURE, id='syntaxerror'),
    pytest.param(RUNTIME_ERROR, utila.FAILURE, id='runtimeerror'),
])
def test_script_execution(code, expected, testdir):
    root = str(testdir)
    script = os.path.join(root, 'source.py')
    utila.file_create(script, code)

    outpath = os.path.join(root, 'output.pdf')

    completed = jam.script.run(
        script,
        document=tests.resources.MASTER_72PAGES,
        outpath=outpath,
    )
    assert completed == expected


@pytest.mark.parametrize('path', [
    pytest.param(tests.resources.SCRIPT_SIMPLE_CHANGE, id='change'),
    pytest.param(tests.resources.SCRIPT_SIMPLE_DELETE, id='delete'),
])
def test_script_execution_simple_changes(path, testdir, monkeypatch):
    root = str(testdir)
    outpath = os.path.join(root, 'changed.pdf')
    cmd = f'-i {tests.resources.MASTER_72PAGES} -o {outpath} --script {path}'
    tests.run_success(cmd, monkeypatch=monkeypatch)
