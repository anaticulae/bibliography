# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

from bibliography.reference import freeand

LONGTEXT = """\
Rumph, H.-J., Hapke, U. & John, U. (1997). Lübecker Alkoholabhängigkeits- und
-missbrauchs-Screening-Test. Göttingen: Hogrefe Verlag GmbH & Co. KG.

Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2004). Beweiswert
rechtsmedizinischer Begutachtungskriterien zur Feststellung der relativen
alkoholbedingten Fahruntüchtigkeit. Blutalkohol, 41, 1-10.

Schnabel, Eva (2011). Alcohol and driving-related performance - A
comprehensive meta-analysis focussing the significance of the
nonsignificant. Unveröffentlichte Dissertation, Philosophische Fakultät
II der Julius Maximilians-Universität, Würzburg.

Becker, W.; Ulrich, P.; Botzkowski, T.; Eurich, S. (2015): Data Analytics
in Familienunternehmen – Implikationen für das Controlling, in:
Zeitschrift für erfolgsorientierte Unternehmenssteuerung, Heft 27, 2015,
S. 263–268

Hahn, Hans Henning; Traba, Robert (Hrsg.) (2012-2015): Deutsch-Polnische
Erinnerungsorte. I. Geteilt/Gemeinsam; Deutsch-Polnische Erinnerungsorte
II. Geteilt gemeinsam; Deutsch-Polnische Erinnerungsorte III.
Parallelen; Deutsch-Polnische Erinnerungsorte IV. Reflexionen;
DeutschPolnische Erinnerungsorte V. Erinnerung auf Polnisch. Texte zu
Theorie und Praxis des sozialen Gedächtnisses. Paderborn u.a.:
Schöningh.

Keller, Thomas (2007a): Die Sainte Victoire – ein deutsch-französischer
Ort und seine Schatten. Cahiers d’Etudes Germaniques 53, H. 2, 93-122.

BOUS K. (1933): 900 Jahre Neunkirchen. Kurze chronologische Geschichte
von 1036-1930. - Neunkirchen

BOBEK H., FESL M. (1978): Das System der zentralen Orte Österreichs:
Eine empirische Untersuchung - Graz

Wessels, Wolfgang, 2007: Die Europapolitik in der wissenschaftlichen
Debatte. In: Weidenfeld, Werner / Wessels, Wolfgang (Hrsg.): Jahrbuch
der Europäischen Integration 2006. Baden-Baden: Nomos
Verlagsgesellschaft, 1. Auflage, S. 27 - 38.

Latham L. & Lundy B. (March 8, 2006). Podcasting is new and suoer nice.
More nice.

Lorenz, Sascha (2001:) Text Mining – Methoden und Techniken.
Diplomarbeit an der Technischen Universität Dresden.

Hug, T. & Poscheschnik, G. (2010). Empirisch Forschen. Die Planung und \
Umsetzung von Projekten im Studium (Studieren, aber richtig. UTB 3357: \
Schl\xFCsselkompetenzen). Konstanz: UVK.

Hawaiian Dictionaries. (2012). Wiki [On-line]. Available: \
wehewehe.org/gsdl2.5/cgi-bin/hdict?d=D21021

Rapoport, A., Chammah, M: (1965): Prisoner’s Dilemma – A Study in \
Conflict and Cooperation. Ann Arbor: . University of Michigan Press.
""".split('\n\n')

LONGTEXT_EXPECTED = [
    (
        'Lübecker Alkoholabhängigkeits- und -missbrauchs-Screening-Test',
        [['Rumph', 'H.-J.'], ['Hapke', 'U.'], ['John', 'U.']],
        None,
        1997,
        None,
    ),
    (
        ('Beweiswert rechtsmedizinischer Begutachtungskriterien zur '
         'Feststellung der relativen alkoholbedingten Fahruntüchtigkeit'),
        [['Schmidt', 'R.'], ['Dettmeyer', 'R.'], ['Padosch', 'S.'],
         ['Madea', 'B.']],
        (1, 10),
        2004,
        None,
    ),
    (
        ('Alcohol and driving-related performance - A comprehensive '
         'meta-analysis focussing the significance of the nonsignificant'),
        [['Schnabel', 'Eva']],
        None,
        2011,
        None,
    ),
    (
        None,
        [['Becker', 'W.'], ['Ulrich', 'P.'], ['Botzkowski', 'T.'],
         ['Eurich', 'S.']],
        (263, 268),
        2015,
        None,
    ),
    (
        None,
        [['Hahn', 'Hans Henning'], ['Traba', 'Robert (Hrsg.)']],
        None,
        2012,
        None,
    ),
    (
        'Die Sainte Victoire – ein deutsch-französischer Ort und seine Schatten',
        [['Keller', 'Thomas']],
        (93, 122),
        2007,
        None,
    ), (
        None,
        [['BOUS', 'K.']],
        None,
        None,
        None,
    ), (
        None,
        [['BOBEK', 'H.'], ['FESL', 'M.']],
        None,
        None,
        None,
    ), (
        None,
        [['Wessels', 'Wolfgang']],
        None,
        None,
        None,
    ), (None, None, None, None, None),
    (
        None,
        [['Lorenz', 'Sascha']],
        None,
        2001,
        None,
    ), (
        None,
        [['Hug', 'T.'], ['Poscheschnik', 'G.']],
        None,
        2010,
        None,
    ), (
        None,
        [['Hawaiian', 'Dictionaries.']],
        None,
        2012,
        None,
    ), (
        None,
        [['Rapoport', 'A.'], ['Chammah', 'M.']],
        None,
        1965,
        None,
    )
]


@pytest.mark.parametrize('text, title, authors, pages, year, publisher', [
    pytest.param(
        *[LONGTEXT[index]] + list(item),
        id=str(index),
    ) for index, item in enumerate(LONGTEXT_EXPECTED)
])
def test_parse_freeand_long(text, title, authors, pages, year, publisher):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    assert extracted
    if title:
        assert extracted.title == title
    if pages:
        assert extracted.page == pages[0]
        if len(pages) == 2:
            assert extracted.pageend == pages[1]
    if year:
        assert extracted.year == year
    if authors:
        authors = [
            iamraw.Person(name=author[0], firstname=' '.join(author[1:]))
            for author in authors
        ]
        assert extracted.authors == authors or not authors


LONGTEXT_NOPERSON = """\
Deutsche Norm DIN 1422, Teil 1 (1983). Veröffentlichungen aus
Wissenschaft, Technik, Wirtschaft und Verwaltung. Gestaltung von
Manuskripten und Typoskripten. Berlin: Beuth

Duden. Rechtschreibung (2004). Hrsg. von der Dudenredaktion. 23. neu
bearb. Aufl.. Mannheim et al.: Dudenverlag. (Der Duden Bd. 1)
""".split('\n\n')


# yapf:disable
@pytest.mark.parametrize('text, title, authors, pages, year, publisher', [
    pytest.param(
        LONGTEXT_NOPERSON[0],
        None,
        [iamraw.NoPerson(confidence=None, raw='Deutsche Norm DIN 1422, Teil 1')],
        None,
        1983,
        None,
        id='din1422',
    ),
    pytest.param(
        LONGTEXT_NOPERSON[1],
        None,
        [iamraw.NoPerson(confidence=None, raw='Duden. Rechtschreibung')],
        None,
        2004,
        None,
        id='duden2004',
    ),
])
# yapf:enable
def test_parse_freeand_noperson(text, title, authors, pages, year, publisher):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    assert extracted
    if title:
        assert extracted.title == title
    if pages:
        assert extracted.page == pages[0]
        if len(pages) == 2:
            assert extracted.pageend == pages[1]
    if year:
        assert extracted.year == year
    assert extracted.authors == authors or not authors


LONGTEXT_LINK = """\
Trim, John; North, Brian; Coste, Daniel (2001): Gemeinsamer Europäischer
Referenzrahmen für Sprachen: lernen, lehren, beurteilen.
http://student.unifr.ch/pluriling/assets/files/Referenzrahmen2001.pdf
Berlin; München: Langenscheidt KG.

Stratenschulte, Eckart D. (2014): Gründung der Europäischen
Gemeinschaften.
http://www.bpb.de/internationales/europa/europaeische-union/42989/europaeischegemeinschaften?p=all
(27.05.2018).

Macron, Emmanuel; Merkel, Angela (2018): Die deutsch-französische
Freundschaft geht alle etwas an!
https://www.youtube.com/watch?v=RXbcAYxuZxw (23.08.2018).

Landeszentrale für politische Bildung Baden-Württemberg (o.J.): Der
Elysée-Vertrag. https://www.lpb-bw.de/elysee-vertrag.html (01.07.2018).

Bundeskanzleramt Österreich (Hrsg.) (1992): Zentrale Orte Raumordnungsprogramm (NÖ)
https://www.ris.bka.gv.at/Dokumente/LgblNO/LRNI_1992062/LRNI_1992062.pdf (25.01.2018)
""".split('\n\n')


@pytest.mark.parametrize('text, authors, year, hyperlink, accessed, title', [
    pytest.param(
        LONGTEXT_LINK[0],
        None,
        2001,
        'http://student.unifr.ch/pluriling/assets/files/Referenzrahmen2001.pdf',
        None,
        None,
        id='trim',
    ),
    pytest.param(
        LONGTEXT_LINK[1],
        [['Stratenschulte', 'Eckart D.']],
        2014,
        'http://www.bpb.de/internationales/europa/europaeische-union/42989/europaeischegemeinschaften?p=all',
        (2018, 5, 27),
        None,
        id='stratenschulte',
    ),
    pytest.param(
        LONGTEXT_LINK[2],
        [['Macron', 'Emmanuel'], ['Merkel', 'Angela']],
        2018,
        'https://www.youtube.com/watch?v=RXbcAYxuZxw',
        (2018, 8, 23),
        None,
        id='macron',
    ),
    pytest.param(
        LONGTEXT_LINK[3],
        None,
        'no year',
        'https://www.lpb-bw.de/elysee-vertrag.html',
        (2018, 7, 1),
        None,
        id='landeszentrale',
    ),
    pytest.param(
        LONGTEXT_LINK[4],
        None,
        1992,
        'https://www.ris.bka.gv.at/Dokumente/LgblNO/LRNI_1992062/LRNI_1992062.pdf',
        (2018, 1, 25),
        'Zentrale Orte Raumordnungsprogramm (NÖ)',
        id='raumordnung',
    ),
])
def test_parse_freeand_with_link(
    text,
    authors,
    year,
    hyperlink,
    accessed,
    title,
):  # pylint:disable=W0613
    extracted = freeand.parse_longtext(text)
    assert extracted.year == year
    assert extracted.hyperlink in (hyperlink, [hyperlink])
    # TODO: ENABLE ACCESSED LATER!
    # assert extracted.accessed == accessed  # pylint:disable=E1101
    assert extracted.title == title or title is None


NEGATIVE = """\
[Jaa13] Jaafar, A.: A Systemic Approach Integrating Driving Cycles for
the Design ofHybrid Locomotives. In: TRANSACTIONS ON VEHICULAR
TECHNOLOGY(2013), S. 3541 ▒ 3550.
http://dx.doi.org/10.1109/TVT.2013.2267099. ▒DOI
10.1109/TVT.2013.2267099

[Tsc12] Tschöke, H.: Informationsreihe MTZ Wissen Die Elektrifizierung
des Antriebsstrangs 1. Hybridantriebe Definition, Lösungsvarianten. In: MTZ - Motortechnische Zeitschrift (2012).
http://dx.doi.org/10.1007/s35146-012-0327-0. - DOI 10.1007/s35146/012/0327/0
""".split('\n\n')


@pytest.mark.parametrize('text', [
    pytest.param(NEGATIVE[0], id='jaa13'),
    pytest.param(NEGATIVE[1], id='tsc12'),
])
def test_parse_freeand_negative(text):
    extracted = freeand.parse_longtext(text)
    assert not extracted
