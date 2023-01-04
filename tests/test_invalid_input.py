# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import tests


@utilatest.requires(power.BACHELOR056_PDF)
def test_unconnected_pages(td, mp, capsys):
    source = power.link(power.BACHELOR056_PDF)
    pages = '1,2,3,6,7,8'  # invalid pages input

    command = f'-i {source} -o {td.tmpdir} --pages={pages}'
    tests.run(command, mp=mp)

    stdout = utilatest.stdout(capsys)
    assert 'more than one potential bib section' in stdout
