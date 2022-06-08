# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import pytest
import serializeraw
import utila
import utilatest

import bibliography
import tests

ARCHIVE = utila.join(bibliography.ROOT, 'tests/expected', exist=True)


@utilatest.longrun
@pytest.mark.parametrize('source, pages', [
    pytest.param(power.BACHELOR051_PDF, '42:46', id='bachelor051'),
    pytest.param(power.BACHELOR056_PDF, '49:53', id='bachelor056'),
    pytest.param(power.BACHELOR063_PDF, '59', id='bachelor063'),
    pytest.param(power.BACHELOR067_PDF, '63:66', id='bachelor067'),
    pytest.param(power.BACHELOR075_PDF, '70:75', id='bachelor075'),
    pytest.param(power.BACHELOR090_PDF, '84:89', id='bachelor090'),
    pytest.param(power.BACHELOR109_PDF, '72:79', id='bachelor109'),
    pytest.param(power.BACHELOR111_PDF, '85:87', id='bachelor111'),
    pytest.param(power.BACHELOR128_PDF, '96:103', id='bachelor128'),
    pytest.param(power.BACHELOR241_PDF, '239,240', id='bachelor241'),
    pytest.param(power.DISS143_PDF, '131', id='diss143p131'),
    pytest.param(power.DISS143_PDF, '131:143', id='diss143'),
    pytest.param(power.DISS148_PDF, '137:146', id='diss148'),
    pytest.param(power.DISS167_PDF, '140:167', id='diss167'),
    pytest.param(power.DISS170_PDF, '150:163', id='diss170'),
    pytest.param(power.DISS172_PDF, '152:172', id='diss172'),
    pytest.param(power.DISS178_PDF, '166:170', id='diss178'),
    pytest.param(power.DISS266_PDF, '215:247', id='diss266'),
    pytest.param(power.DISS272_PDF, '259:271', id='diss272'),
    pytest.param(power.MASTER072_PDF, '65:71', id='master072'),
    pytest.param(power.MASTER075_PDF, '70', id='master075'),
    pytest.param(power.MASTER083_PDF, '75:82', id='master083'),
    pytest.param(power.MASTER083_PDF, '81', id='master083last'),
    pytest.param(power.MASTER089_PDF, '70:81', id='master089'),
    pytest.param(power.MASTER091B_PDF, '82:89', id='master091b'),
    pytest.param(power.MASTER110_PDF, '104:109', id='master110'),
    pytest.param(power.MASTER116_PDF, '97,98,99,100', id='master116'),
    pytest.param(power.MASTER148_PDF, '109:114', id='master148'),
    pytest.param(power.MASTER155_PDF, '75:85', id='master155'),
    pytest.param(power.ORDER107_PDF, '104:108', id='order107'),
])
def test_validate(source, pages, testdir, monkeypatch):
    testid = utilatest.testid()
    BibCompare(
        source,
        pages,
        testid,
        testdir,
        monkeypatch,
    ).evaluate()


class BibCompare(utilatest.BaseLiner):

    def __init__(self, source, pages, index, testdir, monkeypatch):
        super().__init__(
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            step='',
            source=source,
            pages=pages,
            workdir=testdir.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_bibliography_reference,
            index=index,
        )

    def raw(self, value) -> str:
        return bibtable_raw(value)


def bibtable_raw(value: list) -> str:
    authors = [
        utila.from_tuple(
            item=[item.raw for item in line.authors],
            separator=' ; ',
        ) for line in value
    ]
    authors = [item.strip() for item in authors]
    titles = [
        '    ' + utila.normalize_whitespaces(item.title) if item.title else ''
        for item in value
    ]
    connected = [f'strategy:{value.__strategy__}\n']
    for author, title in zip(authors, titles):
        if not any((author, title)):
            continue
        connected.append(author)
        connected.append(title)
        connected.append('')
    result = utila.NEWLINE.join(connected).strip()
    return result
