# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
[1] W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G. Teubner
Stuttgart, 1994.

[2] M. Baccar, L.A. Gee, R.C. Gonzalez, and
M.A. Abidi. Segmentation of Range Images via Data Fusion and
Morphological Watersheds. Pattern Recognition, 29(10):1673 – 1687, 1996.

[3] W. Bailer, F. Höller, A. Messina, D. Airola, P. Schallauer, and M.
Hausenblas. State of the Art of Content Analysis Tools for Video, Audio
and Speech. Technical report, Presto Space, 3 2005.

>>> len(content('R. Chougule, D. Rajpathak, P. Bandyopadhyay, „An integrated based-reasoning“, '
... 'Computers in Industry, Bd. 62, Nr. 7, S. 742–754, 2011, issn: 0166-3615.').authors)
3

"""

import re

import configo
import german
import iamraw
import utila

import bibliography.quotes


@utila.cacheme
def nosplit(raw: str) -> iamraw.BibliographyReference:
    parsed = content(raw)
    if not parsed:
        return None
    return parsed


@utila.cacheme
def parse(raw: str) -> iamraw.BibliographyReference:
    """\
    >>> parse('[1] Ahrens, Thomas ; Hanke, Hans-Joachim ; Scheel, Wolfgang: '
    ... 'Baugruppentechnologie der Elektronik. 2., aktualisierte u. erw. Berlin '
    ... ': Verl. Technik [u.a.], 1999 http://www.worldcat.org/oclc/634169319. – ISBN 3341012346')
    """
    splitted = split(raw)
    if not splitted:
        return None
    number, text = splitted
    parsed = content(text)
    if not parsed:
        utila.debug(f'could not parse reference:number `{text}`')
        return None
    parsed.reference = f'[{number}]'
    return parsed


SPLITTER = utila.compiles(r"""
    ^
    (?:
        \[(\d{1,4})\]|       # [1] W. Abmayr.
        (\d{1,4})\.          # 4. Guy, G.P., Thomas
    )
    [ ]{0,4}
""")


@utila.cacheme
def split(raw: str) -> tuple:
    """\
    >>> split('[1] W. Abmayr. Einführung in die digitale')
    (1, 'W. Abmayr. Einführung in die digitale')
    >>> split('4. Guy, G.P., Thomas, C.C., Thompson, T., Watson, M., Massetti, G.M.')
    (4, 'Guy, G.P., Thomas, C.C., Thompson, T., Watson, M., Massetti, G.M.')
    """
    splitted = SPLITTER.split(raw)
    if len(splitted) == 1:
        # not splitted
        return None
    try:
        number = int(splitted[1])
    except TypeError:
        number = int(splitted[2])
    data = splitted[3]
    return number, data


PATTERN = utila.compiles(r"""
    ^
    (?P<authors>
        (
            (\w\.[ ]{0,3}){1,2}             # short first name
            \w{2,}                          # last name
            (\,|\.){0,1}                    # optional separator between authors
            ([ ]{0,3}\band\b[ ]{0,3}){0,1}  # optional and before last author
            [ ]{0,3}
        ){1,}                               # more than one author
    )
    [ ]{0,3}
    (?P<middle>.+?)
    \,{0,1}
    [ ]{0,3}
    (?P<year>(20[012]\d|1[789]\d\d))
    [ ]{0,3}
    \.{0,1}
""")

TITLE_LENGTH_MIN = configo.HV_INT_PLUS(default=10)


@utila.cacheme
def content(
    raw: str,
    title_length_min: int = TITLE_LENGTH_MIN,
) -> iamraw.BibliographyReference:
    """\
    >>> content('W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G. Teubner Stuttgart, 1994.')
    BibliographyReference(title='Einf...year=1994...name='Abmayr.'...)
    >>> content('M. Baccar, L.A. Gee, R.C. Gonzalez, and M.A. Abidi. Segmentation of Range Images via, 1996.')
    BibliographyReference(title='Segmentat...year=1996...)
    >>> content('D. Forsyth and J. Ponce. Computer Vision. A Modern Approch. Prentice Hall PTR, 2002.')
    BibliographyReference(title='Computer Vision'...year=2002,...)
    """
    parsed = PATTERN.search(raw)
    if parsed:
        authors = parsed['authors']
        authors = improve_raw(authors)
        authors = german.authors(authors)
        authors = german.authors_decide(authors)
        year = int(parsed['year'])
        middle = parsed['middle']
        raw = utila.extract_match(parsed)
    else:
        # backup strategy
        try:
            authors, middle = search_author(raw)
        except TypeError:
            return None
        if not authors:
            return None
        year = None
    result = iamraw.BibliographyReference(
        authors=authors,
        year=year,
        raw=raw,
    )
    if middle:
        try:
            title, middle = middle.split('.', maxsplit=1)
        except ValueError:
            # no dot in middle
            title, middle = middle, ''
        if len(title) > title_length_min:
            result.title = title
        result.data = middle.strip()
    return result


@utila.cacheme
def improve_raw(authors: str) -> str:
    """\
    >>> improve_raw('Grunwald Armin; Gerhard Banse; Christopher Coenen und Leonhard Hennen')
    'Grunwald Armin; Gerhard Banse; Christopher Coenen ; Leonhard Hennen'
    """
    separator = ',' if authors.count(',') >= authors.count(';') else ';'
    authors = re.sub(r'\b(and|und)\b', f'{separator}', authors)
    authors = authors.strip(',; ')
    return authors


@utila.cacheme
def search_author(raw: str):
    """\
    >>> search_author('N. Jakob, S. H. Weber, M. C. Müller, I. Gurevych, „Beyond the stars: exploiting free-text“')
    ([Person(name='Jakob', firstname='N.',...ing free-text“')
    """
    removed = bibliography.quotes.before_first_quote(raw)
    if removed is None:
        return None
    # TODO: HACK Y COLLECTOR
    possible_endings = utila.findindex(removed, ' ')
    best = []
    for index in possible_endings:
        text = removed[0:index].replace(',', ';')
        authors = german.authors(text)
        authors = [item[0].split() for item in authors]
        authors: list = german.authors_decide(authors)
        # remove noperson
        authors = [item for item in authors if isinstance(item, iamraw.Person)]
        if len(authors) > len(best):
            best = authors
    for item in best:
        raw = raw.replace(item.raw, '')
    raw = raw.strip(',;: ')
    return best, raw
