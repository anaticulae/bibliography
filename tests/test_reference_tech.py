# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import utila

import bibliography.label
import bibliography.reference.tech

CONTENT = """\
Verknüpfung klassisches und AUTOSAR-Steuergerät
linearer Bus und ein Einzelstern nach [WL11]
Pegel bei der NRZ-Datenübertragung
Nominelle Potentiale nach [WR10, Seite 214]
Buszugriff Abitrierungsphase nach [WR10, Seite 216]
CAN-Nachricht nach [WL11, Seite 19]
Codegenerierung nach [Rum05, Seite 62]
der Zugriffe nach [JL07, Seite 389]
[VAC+08]
[mat12b]
[Sch05, Seite 3-4]
[ Ju04] JUERGEN LEOHOLD:
[K.11] K., Pengutronix e.: How to become a PTXdist Guru - Based on the
OSELAS.BSP( ) -Pengutronix Generic-arm. August 2011
Weiss führt zu den Kernfunktionen noch den Begriff Prediction (Prognose)
für Text Categorization ein ([We05], S. 48). Weiss et al. behandeln in
([WIZ12]) die vier Gebiete Document Classification
"""

EXPECTED = """\
([We05], S. 48)
([WIZ12])
[WL11]
[WR10, Seite 214]
[WR10, Seite 216]
[WL11, Seite 19]
[Rum05, Seite 62]
[JL07, Seite 389]
[VAC+08]
[mat12b]
[Sch05, Seite 3-4]
[ Ju04]
[K.11]
"""


def test_parse_tech():
    extracted = bibliography.label.parses(CONTENT)
    assert len(extracted) == len(EXPECTED.splitlines())
    current = utila.NEWLINE.join((item.raw for item in extracted))
    assert current == EXPECTED.strip()


LONGTEXT = """\
EPA: Locomotive emission standards: regulatory support document. Office
of Mobile Sources, Office of Air and Radiation, U.S. Environmental
Protection Agency, 1999

Donnelly, F.: Hybrid technology for the rail industry. In: Rail
Conference, 2004. Proceedings of the 2004 ASME/IEEE Joint, 2004, S.
113–117

IAV: Zusammenfassung Datenanalyse. 2015

Lindemann, M ; Gühmann, C: VeLoDyn - Ein Werkzeug zur
Triebstrangsimulation von Kraftfahrzeugen. In: 1. Tagung Simulation und
Test in der Funktionsund Softwareentwicklung, 2003, 1-11

Gasper, R.: Flachheitsbasierter Vorsteuerungsentwurf für den
Antriebsstrang eines Parallelhybridfahrzeuges. VDI Verlag GmbH, 2013
(VDI-Buch)

Dittmann, D.: Alstom Hybridlokomotiven im Verschubeinsatz - Konzept und
Erfahrungen im Einsatz H3 Fahrzeugplattform. 2013

Heißing, B.: Fahrwerkhandbuch: Grundlagen · Fahrdynamik · Komponenten ·
Systeme · Mechatronik · Perspektiven. Springer Fachmedien Wiesbaden,
2013 (ATZ/MTZ-Fachbuch)
""".split('\n\n')

# pylint:disable=E1101


@pytest.mark.parametrize('text, title, authors, pages, year, publisher', [
    pytest.param(
        LONGTEXT[0],
        'Locomotive emission standards: regulatory support document',
        [iamraw.NoPerson(raw='EPA')],
        None,
        1999,
        'Office of Mobile Sources, Office of Air and Radiation, U.S. Environmental Protection Agency',
        id='epa',
    ),
    pytest.param(
        LONGTEXT[1],
        'Hybrid technology for the rail industry',
        [iamraw.Person('Donnelly', 'F.', raw='Donnelly F.')],
        (113, 117),
        2004,
        'Rail Conference, 2004. Proceedings of the 2004 ASME/IEEE Joint',
        id='donelly',
    ),
    pytest.param(
        LONGTEXT[2],
        'Zusammenfassung Datenanalyse',
        [iamraw.NoPerson(raw='IAV')],
        None,
        2015,
        None,
        id='iav',
    ),
    pytest.param(
        LONGTEXT[3],
        'VeLoDyn - Ein Werkzeug zur Triebstrangsimulation von Kraftfahrzeugen',
        [
            iamraw.Person('Lindemann', 'M', raw='Lindemann M'),
            iamraw.Person('Gühmann', 'C', raw='Gühmann C'),
        ],
        None,
        2003,
        None,
        id='velodyn',
    ),
    pytest.param(
        LONGTEXT[4],
        'Flachheitsbasierter Vorsteuerungsentwurf für den Antriebsstrang eines Parallelhybridfahrzeuges',
        [iamraw.Person('Gasper', 'R.', raw='Gasper R.')],
        None,
        2013,
        None,
        id='gasper',
    ),
    pytest.param(
        LONGTEXT[6],
        'Fahrwerkhandbuch: Grundlagen · Fahrdynamik · Komponenten · Systeme · Mechatronik · Perspektiven',
        [iamraw.Person('Heißing', 'B.', raw='Heißing B.')],
        None,
        2013,
        None,
        id='heissing',
    ),
])
def test_parse_tech_long(text, title, authors, pages, year, publisher):  # pylint:disable=W0613
    extracted = bibliography.reference.tech.parse_longtext(text)
    if title:
        assert extracted.title == title
    if pages:
        assert extracted.page == pages[0]
        if len(pages) == 2:
            assert extracted.pageend == pages[1]
    if year:
        assert extracted.year == year
    if authors:
        assert extracted.authors == authors


NO_PERSON = 'OHMEDA MEDIZINTECHNIK: 2300 Finapress Blutdruckmonitor; Bedienungsanleitung,Puchheim (1991)'


def test_parse_no_person():
    extracted = bibliography.reference.tech.parse_longtext(NO_PERSON)
    assert extracted.title
    assert extracted.authors
