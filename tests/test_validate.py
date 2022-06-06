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


def bachelor51(flat):
    assert len(flat) == 37  # VALIDATED


def bachelor90(flat):
    references = [item.reference for item in flat]
    expected = [
        'Ju04', 'AT09', 'Bae08', 'BAU11', 'BKL+09', 'Bus98', 'But11', 'CJM12',
        'Dav72', 'DDG09', 'DIN08', 'Dor10', 'DRP01', 'emf12', 'FLS07', 'Fos10',
        'Güe06', 'Hal93', 'Hof08', 'Hue10', 'Ibr04', 'ISO03', 'ISO05', 'JL07',
        'K.11', 'Lig09', 'Mar07', 'Mat09', 'mat12a', 'mat12b', 'mat12c',
        'mis98', 'NN09', 'OK09', 'Ole10', 'Plu06', 'PP04', 'PR06', 'Rei12',
        'Rum05', 'SBD+10', 'Sch05', 'Sta73', 'Sta09', 'Ste12', 'TS07', 'TZ10',
        'VAC+08', 'VG06', 'WL11', 'WR10', 'ZSM11'
    ]
    assert references == expected


def master75(flat):  # pylint:disable=W0613
    pass


def master110(flat):
    titles = [item.title for item in flat if item.title]
    assert len(titles) >= 66  # NOT VALIDATED


def master116(flat):
    expected = [
        'App14', 'Bah12', 'Bas14', 'Bor13', 'Bra11', 'Dit13', 'Don04', 'EB03',
        'EPA98', 'Fil15', 'Fis12', 'Fri15', 'Gas13', 'Gev13', 'Hei13', 'Hof11',
        'IAV15', 'Jaa13', 'Kac14', 'Kon13', 'Kur16', 'Les15', 'LG03', 'Mü13',
        'Mag14', 'MAT16', 'Min13', 'Mor09', 'Nit11', 'Pac12', 'Pap15', 'Pfe14',
        'Rö15', 'Rei10', 'Rie11', 'RNB12', 'Sch09', 'Sko11', 'Spi05', 'Stö10',
        'Tom12', 'Tsc12', 'Vö15', 'Wik07', 'Wik13', 'Wit13'
    ]
    references = [item.reference for item in flat]
    assert references == expected
    authors = [item.authors for item in flat]
    assert authors


def diss170(flat):
    # 11+11+11+12+11+11+11+11+11+13+11+13+5
    assert len(flat) == 145  # change to 142!


def diss272(flat):
    # 11 11 11 9 10 11 11 11 12 11 12 3 = 124
    assert len(flat) == 116  # TODO: CHANGES LATER


def bachelor128(flat):
    assert flat
    # 51: Validated by hand
    assert len(flat) == 47
    assert all(isinstance(item.year, (int)) for item in flat if item.year)


def master91b(flat):
    assert flat
    assert len(flat) == 85  # VALIDATED


def master148(flat):
    assert flat


# yapf:disable
@pytest.mark.parametrize('source, pages, expected, validate', [
    pytest.param(power.BACHELOR051_PDF, '42:46', 37, bachelor51, id='bachelor051'),
    pytest.param(power.BACHELOR056_PDF, '49:53', 32, 'bachelor056', id='bachelor056'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR063_PDF, '59', 'bachelor063', 'bachelor063', id='bachelor063'),
    pytest.param(power.BACHELOR067_PDF, '63:66', None, 'bachelor067', id='bachelor067'),
    pytest.param(power.BACHELOR075_PDF, '70:75', None, 'bachelor075', id='bachelor075'),
    pytest.param(power.BACHELOR090_PDF, '84:89', 52, bachelor90, id='bachelor090'),
    pytest.param(power.BACHELOR109_PDF, '72:79', 98, 'bachelor109', id='bachelor109'),
    pytest.param(power.BACHELOR111_PDF, '85:87', 18, 'bachelor111', id='bachelor111'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR128_PDF, '96:103', None, bachelor128, id='bachelor128'),
    pytest.param(power.BACHELOR241_PDF, '239,240', None, 'bachelor241', id='bachelor241'),
    pytest.param(power.DISS143_PDF, '131', None, 'diss143p131', id='diss143p131'),
    pytest.param(power.DISS143_PDF, '131:143', None, 'diss143', id='diss143'),
    pytest.param(power.DISS148_PDF, '137:146', None, 'diss148', id='diss148'),
    pytest.param(power.DISS167_PDF, '140:167', None, 'diss167', id='diss167'),
    pytest.param(power.DISS170_PDF, '150:163', None, 'diss170', id='diss170'),
    pytest.param(power.DISS172_PDF, '152:172', None, 'diss172', id='diss172'),
    pytest.param(power.DISS178_PDF, '166:170', None, 'diss178', id='diss178'),
    pytest.param(power.DISS266_PDF, '215:247', 427, None, id='diss266', marks=pytest.mark.xfail(reason='improve parser')), # VALIDATED BY HAND
    pytest.param(power.DISS272_PDF, '259:271', None, diss272, id='diss272'),
    pytest.param(power.MASTER072_PDF, '65:71', None, 'master072', id='master072'),
    pytest.param(power.MASTER075_PDF, '70', 18, master75, id='master075'), # VALIDATED BY HAND
    pytest.param(power.MASTER083_PDF, '75:82', None, 'master083', id='master083'),
    pytest.param(power.MASTER083_PDF, '81', 'master083last', 'master083last', id='master083last'),
    pytest.param(power.MASTER089_PDF, '70:81', 149, 'master089', id='master089'), # VALIDATED BY HAND
    pytest.param(power.MASTER091B_PDF, '82:89', 85, master91b, id='master091b'), # VALIDATED BY HAND
    pytest.param(power.MASTER110_PDF, '104:109', 70, master110, id='master110'),
    pytest.param(power.MASTER116_PDF, '97,98,99,100', 46, master116, id='master116'), # VALIDATED BY HAND
    pytest.param(power.MASTER148_PDF, '109:114', 38, master148, id='master148', marks=pytest.mark.xfail(reason='improve parser')), # VALIDATED BY HAND
    pytest.param(power.MASTER155_PDF, '75:85', None, 'master155', id='master155'), # VALIDATED BY HAND 109
    pytest.param(power.ORDER107_PDF, '104:108', 31, 'order107', id='order107'), # VALIDATED BY HAND
])
# yapf:enable
@utilatest.longrun
def test_validate(
    source,
    pages,
    expected,
    validate,
    testdir,
    monkeypatch,
):
    BibCompare(
        source,
        pages,
        expected,
        validate,
        testdir,
        monkeypatch,
    ).evaluate()


class BibCompare(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, validate, testdir, monkeypatch):
        super().__init__(
            program=functools.partial(tests.run, monkeypatch=monkeypatch),
            step='',
            source=source,
            pages=pages,
            workdir=testdir.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_bibliography_reference,
            index=validate if isinstance(validate, str) else None,
        )
        self.numbers = expected
        self.validate = validate

    def raw(self, value) -> str:
        return bibtable_raw(value)

    def evaluate(self):
        super().evaluate()
        flat = self.load().references
        if isinstance(self.numbers, int):
            assert len(flat) == self.numbers
        if callable(self.validate):
            self.validate(flat)

    def backup(self, value):
        flat = utila.flatten(value)
        assert len(flat) == self.numbers or self.numbers is None
        if isinstance(self.numbers, int):
            assert len(flat) == self.numbers
        elif self.validate:
            self.validate(flat)


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


@utilatest.requires(power.BACHELOR037_PDF)
def test_bib_headline_bachelor037(testdir, monkeypatch):
    source = power.link(power.BACHELOR037_PDF)
    cmd = f'-i {source} -o {testdir.tmpdir} --pages=33'
    tests.run(cmd, monkeypatch=monkeypatch)
    table = serializeraw.load_bibliography_reference(content=testdir.tmpdir)
    assert table.headline == 'Literaturangaben'
    assert table.pdfpages == (33,)
