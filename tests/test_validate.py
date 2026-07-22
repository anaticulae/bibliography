# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import bibliography
import tests

ARCHIVE = utilo.join(bibliography.ROOT, 'tests/expected', exist=True)


@utilotest.longrun
@pytest.mark.parametrize('source, pages', [
    pytest.param(hoverpower.BACHELOR051_PDF, '42:46', id='bachelor051'),
    pytest.param(hoverpower.BACHELOR056_PDF, '49:53', id='bachelor056'),
    pytest.param(hoverpower.BACHELOR063_PDF, '59', id='bachelor063'),
    pytest.param(hoverpower.BACHELOR067_PDF, '63:66', id='bachelor067'),
    pytest.param(hoverpower.BACHELOR075_PDF, '70:75', id='bachelor075'),
    pytest.param(hoverpower.BACHELOR090_PDF, '84:89', id='bachelor090'),
    pytest.param(hoverpower.BACHELOR109_PDF, '72:79', id='bachelor109'),
    pytest.param(hoverpower.BACHELOR111_PDF, '85:87', id='bachelor111'),
    pytest.param(hoverpower.BACHELOR128_PDF, '96:103', id='bachelor128'),
    pytest.param(hoverpower.BACHELOR241_PDF, '239,240', id='bachelor241'),
    pytest.param(hoverpower.DISS143_PDF, '131', id='diss143p131'),
    pytest.param(hoverpower.DISS143_PDF, '131:143', id='diss143'),
    pytest.param(hoverpower.DISS148_PDF, '137:146', id='diss148'),
    pytest.param(hoverpower.DISS167_PDF, '140:167', id='diss167'),
    pytest.param(hoverpower.DISS170_PDF, '150:163', id='diss170'),
    pytest.param(hoverpower.DISS172_PDF, '152:172', id='diss172'),
    pytest.param(hoverpower.DISS178_PDF, '166:170', id='diss178'),
    pytest.param(hoverpower.DISS266_PDF, '215:247', id='diss266'),
    pytest.param(hoverpower.DISS272_PDF, '259:271', id='diss272'),
    pytest.param(hoverpower.MASTER072_PDF, '65:71', id='master072'),
    pytest.param(hoverpower.MASTER075_PDF, '70', id='master075'),
    pytest.param(hoverpower.MASTER083_PDF, '75:82', id='master083'),
    pytest.param(hoverpower.MASTER083_PDF, '81', id='master083last'),
    pytest.param(hoverpower.MASTER089_PDF, '70:81', id='master089'),
    pytest.param(hoverpower.MASTER091B_PDF, '82:89', id='master091b'),
    pytest.param(hoverpower.MASTER110_PDF, '104:109', id='master110'),
    pytest.param(hoverpower.MASTER116_PDF, '97,98,99,100', id='master116'),
    pytest.param(hoverpower.MASTER148_PDF, '109:114', id='master148'),
    pytest.param(hoverpower.MASTER155_PDF, '75:85', id='master155'),
    pytest.param(hoverpower.ORDER107_PDF, '104:108', id='order107'),
])
def test_validate(source, pages, td, mp):
    utilotest.fixture_requires(source)
    testid = utilotest.testid()
    BibCompare(
        source,
        pages,
        testid,
        td,
        mp,
    ).evaluate()


class BibCompare(utilotest.BaseLiner):

    def __init__(self, source, pages, index, td, mp):
        super().__init__(
            program=functools.partial(tests.run, mp=mp),
            step='',
            source=source,
            pages=pages,
            workdir=td.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_bibliography_reference,
            index=index,
        )

    def raw(self, value) -> str:
        return bibtable_raw(value)


def bibtable_raw(value: list) -> str:
    authors = [
        utilo.from_tuple(
            item=[item.raw for item in line.authors],
            separator=' ; ',
        ) for line in value
    ]
    authors = [item.strip() for item in authors]
    titles = [
        '    ' + utilo.normalize_whitespaces(item.title) if item.title else ''
        for item in value
    ]
    connected = [f'strategy:{value.__strategy__}\n']
    for author, title in zip(authors, titles):
        if not any((author, title)):
            continue
        connected.append(author)
        connected.append(title)
        connected.append('')
    result = utilo.NEWLINE.join(connected).strip()
    return result
