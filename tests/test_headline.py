# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests


@utilatest.requires(power.BACHELOR037_PDF)
def test_bib_headline_bachelor037(testdir, monkeypatch):
    source = power.link(power.BACHELOR037_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --pages=33'
    tests.run(cmd, monkeypatch=monkeypatch)
    table = serializeraw.load_bibliography_reference(content=testdir.tmpdir)
    assert table.headline == 'Literaturangaben'
    assert table.pdfpages == (33,)
