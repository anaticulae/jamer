# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# import functools

# import hoverpower
# import utilo
# import utilotest

# import pdfsmall.cli
# import pdfsmall.optimize
# import tests.pdfsmall_

# small = functools.partial(
#     utilotest.run_cov,
#     process='pdfsmall',
#     main=pdfsmall.cli.main,
#     expect=True,
# )

# @tests.pdfsmall_.hasghost
# @utilotest.nightly
# def test_small(td, mp):
#     source = hoverpower.MASTER116_PDF
#     before = utilo.file_size(source)
#     outpath = td.tmpdir.join('small.pdf')
#     small(cmd=f'-i {source} -o {outpath}', mp=mp)
#     after = utilo.file_size(outpath)
#     assert after < before

# @tests.pdfsmall_.hasghost
# @utilotest.longrun
# def test_ghost(td):
#     source = hoverpower.MASTER116_PDF
#     before = utilo.file_size(source)
#     outpath = td.tmpdir.join('small.pdf')
#     pdfsmall.optimize.ghost_small(source, outpath)
#     after = utilo.file_size(outpath)
#     assert after < before
