# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import bibliography.layout.column


@utilatest.requires(power.BACHELOR063_PDF)
def test_parse_bibliography_bachelor63_page59():
    """Latex double column. Left side with [Hem10] pattern"""
    pages = (59)
    navigators = serializeraw.ptn_frompath(
        power.link(power.BACHELOR063_PDF),
        # fill_empty=False,
        pages=pages,
    )
    parsed = bibliography.layout.column.extracts(navigators)
    parsed = utila.flatten(parsed)
    assert len(parsed) == 12, str(parsed)


@utilatest.longrun
@utilatest.requires(power.BACHELOR037_PDF)
def test_parse_bibliography_bachelor37():
    pages = (33,)
    navigators = serializeraw.ptn_frompath(
        power.link(power.BACHELOR037_PDF),
        pages=pages,
    )
    parsed = bibliography.layout.column.extracts(navigators)
    parsed = utila.flatten(parsed)
    assert len(parsed) == 31, str(parsed)
