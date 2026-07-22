# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import bibliography.layout.alternate


@pytest.mark.parametrize('pages, expected', [
    (97, 14),
    (98, 14),
    (99, 15),
    (100, 3),
])
@utilotest.longrun
@utilotest.requires(hoverpower.MASTER116_PDF)
def test_parse_bibliography_master116_page_x(pages, expected):
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.MASTER116_PDF),
        prefix='oneline',
        pages=pages,
    )
    parsed = bibliography.layout.alternate.extracts(navigators)
    parsed = utilo.flat(parsed)
    assert len(parsed) == expected, str(parsed)


@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_parse_bibliography_hurenkind():
    expected = 7  # VALIDATED; 8 with item from before, but item in not completed
    pages = (51,)
    navigators = serializeraw.ptn_frompath(
        hoverpower.link(hoverpower.BACHELOR056_PDF),
        prefix='oneline',
        pages=pages,
    )
    parsed = bibliography.layout.alternate.extracts(navigators)
    parsed = utilo.flat(parsed)
    assert len(parsed) == expected, str(parsed)


# yapf:disable
ALTERNATE = utilo.splitlines("""\
Adloff, Frank: Zivilgesellschaft – Theorie und politische Praxis.
 Frankfurt/Main: Campus Verlag, 2005.

Aktion Demenz e.V.: Eine Kommune auf dem Weg: Arnsberg.
 (unveröffentlichtes Material)
""", pattern='\n\n')
# yapf:enable
PARAMETERS = [
    pytest.param(item, id=utilotest.simple(item)) for item in ALTERNATE
]


@pytest.mark.parametrize('raw', PARAMETERS)
def test_parse_alternate_single(raw):
    parsed = bibliography.layout.alternate.split_bibliography(raw)
    assert parsed


EBD = """\
— (2005a). ISO 10303-108:2005 - Industrial automation systems and integration Product data
    representation and exchange - Part 108: Integrated application resource: Parameterization
    and constraints for explicit geometric product models.
"""


def test_alternate_ebd():
    parsed = bibliography.layout.alternate.split_bibliography(EBD)
    assert parsed
    assert len(parsed.authors) == 1
    # TODO: VERIFY EBENDIES FLAG
    assert parsed.authors[0].raw == '—'
