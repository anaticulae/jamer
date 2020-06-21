#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import functools

import utilatest

import jam
import jam.cli

#pylint: disable=invalid-name
run_success = functools.partial(
    utilatest.run_command,
    main=jam.cli.main,
    process=jam.PACKAGE,
    success=True,
)

run_failure = functools.partial(
    utilatest.run_command,
    main=jam.cli.main,
    process=jam.PACKAGE,
    success=False,
)
