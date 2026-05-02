# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# import os

# import hoverpower
# import pytest
# import utilo
# import utilotest

# import jamer.script
# import tests.resources

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

# @utilotest.longrun
# def test_script_master(td):
#     script = td.tmpdir.join('master.py')
#     utilo.file_create(script, MASTER)
#     outpath = td.tmpdir.join('output.pdf')
#     completed = jamer.script.run(
#         script,
#         document=hoverpower.MASTER072_PDF,
#         outpath=outpath,
#     )
#     assert completed == utilo.SUCCESS
#     assert os.path.exists(outpath), str(outpath)

# @pytest.mark.parametrize('code, expected', [
#     pytest.param(EXAMPLE, utilo.SUCCESS, id='simple'),
#     pytest.param(SYNTAX_ERROR, utilo.FAILURE, id='syntaxerror'),
#     pytest.param(RUNTIME_ERROR, utilo.FAILURE, id='runtimeerror'),
# ])
# @utilotest.longrun
# def test_script_execution(code, expected, td):
#     script = td.tmpdir.join('source.py')
#     utilo.file_create(script, code)
#     outpath = td.tmpdir.join('output.pdf')
#     completed = jamer.script.run(
#         script,
#         document=hoverpower.MASTER072_PDF,
#         outpath=outpath,
#     )
#     assert completed == expected

# @pytest.mark.parametrize('path', [
#     pytest.param(tests.resources.SCRIPT_SIMPLE_CHANGE, id='change'),
#     pytest.param(tests.resources.SCRIPT_SIMPLE_DELETE, id='delete'),
# ])
# @utilotest.longrun
# def test_script_execution_simple_changes(path, td, mp):
#     outpath = td.tmpdir.join('changed.pdf')
#     cmd = f'-i {hoverpower.MASTER072_PDF} -o {outpath} --script {path}'
#     tests.run(cmd, mp=mp)
