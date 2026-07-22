# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests


@utilotest.requires(hoverpower.BACHELOR037_PDF)
def test_bib_headline_bachelor037(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR037_PDF)
    cmd = f'-i {source} -o {td.tmpdir} --pages=33'
    tests.run(cmd, mp=mp)
    table = serializeraw.load_bibliography_reference(content=td.tmpdir)
    assert table.headline == 'Literaturangaben'
    assert table.pdfpages == (33,)
