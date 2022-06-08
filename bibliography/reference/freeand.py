# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRef AND(&) Parser
====================

.. code-block:: none

    Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2000b). A
    review of the literature on the Effects of Low Doses of Alcohol on
    driving-Related Skills. National Highway Traffic Safety
    Administration (NHTS), Southern California Research Institute,
    Washington.

Authors
-------

Correct
~~~~~~~

* Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B.

Failures
~~~~~~~~

* Schnabel, Eva
* Sdao-Jarvie, K. and Vogel-Sprott, M.

Examples
~~~~~~~~

* master148: very bad bib sources

"""

import configo
import german
import iamraw
import utila


@utila.cacheme
def parse_longtext(
    content: str,
    pattern=None,
) -> iamraw.BibliographyReference:
    content = utila.normalize_text(content)
    pattern = NORMAL if pattern is None else pattern
    raw = content
    matched = utila.search(pattern, content)
    if not matched:
        return None
    authors = select_authors(matched)
    years = select_year(matched)
    number = matched['number'] if matched['number'] else None
    hyperlinks, content = parse_hyperlinks(content)
    accessed, content = parse_accessed(content)
    parsed_title = parse_title(content=matched['content'])
    if not parsed_title:
        return None
    title, rest = parsed_title
    page, pageend, rest = parse_pages(rest)
    title = title.strip(' :,;')
    result = iamraw.BibliographyReference(
        authors=authors,
        number=number,
        title=title,
        year=years[0],
        yearend=years[1],
        page=page,
        pageend=pageend,
        hyperlink=hyperlinks if hyperlinks else None,
        accessed=accessed[0][1] if accessed else None,
        raw=raw,
    )
    return result


MONTH = r"""
    (
        [ ]{0,3}
        (%s)
        [ ]{0,3}
        \d{0,2}
        [ ]{0,3}
        \,{0,1}
        [ ]{0,3}
    ){0,1}
""" % german.MONTH_REGEX

# TODO: ADD OPTIONAL BRACKETS TO REMOVE DIRTY SIMPLE YEAR HACK
# TODO: REMOVE 4,5 HACK: WHEN SUPPORTING HIGHNOTE
AND = r"""
    (?P<authors>
        (
            [A-Z,;:\(\)\.\-\&ÖÄÜß\d\'\/ ]{4,}?
            [^\(\)\[\]]               # author does not ends with bracket
        |
            ^[–— ]{1,3}               # ebd. shortcut
        |   ^Ebd\.?
        )
    )
    (
        \(?(?P<oj>o\.j\.[ ]{0,3}[a-z]{0,1})\)?
        |
        %s                        # brackets open
        %s                        # optional month
        ((?P<year>\d{4,5})([ ]{0,3}\-(?P<yearend>\d{4})){0,1})
        [ ]{0,3}
        (?P<number>a|b|c|d){0,1}  # optional char
        %s                        # brackets close
        |
        \({0,1}
        (?P<simpleyear>\d{4})[ ]{0,2}[a-z]{0,1}[ ]{0,2}:    # see wessels 2007, TODO: DIRTY
        \){0,1}
    )
    [ ]{0,5}                      # remove trailing white spaces
    [:\.]{0,1}                    # remove dot or colon
    [ ]{0,5}                      # remove trailing white spaces
    (?P<content>.+)
"""

NORMAL = AND % (r'\(', MONTH, r'\)')

BROKEN_BRACKETS = AND % (r'[\(\[]', MONTH, r'[\]\)]')
"""\
>>> parse_longtext('Deutsche Norm DIN 1421 (1983]: Abschnitte. Berlin: Beuth', pattern=BROKEN_BRACKETS).authors
[NoPerson(confidence=None, raw='Deutsche Norm DIN 1421')]
"""

NOTITLE = False

TITLE_START = utila.compiles(r'[\.\?\!][ ]')


@utila.cacheme
def parse_title(content: str) -> tuple:  # pylint:disable=R0911,R1260
    """Increase number of valid dots to parse long title with a lot of dots.

    >>> parse_title('Hrsg. von der Dudenredaktion. 23. neu bearb. Aufl..') # TODO: CHANGE LATER
    ('Hrsg. von der Dudenredaktion', '23. neu bearb. Aufl..')
    >>> parse_title('Das System der zentralen Orte Österreichs: Eine empirische Untersuchung - Graz')
    ['Das System der zentralen Orte Österreichs: Eine empirische Untersuchung', 'Graz']
    """
    # 1.  Try normal title splitter
    # 1b. Try splitting till link starts
    # 2.  Extend number of valid dots
    try:
        title, rest = TITLE_START.split(content, maxsplit=1)
        # TODO: INCLUDE SENTENCE SIGN
        if invalid_title(title) == NOTITLE:
            # None means no title given
            return title, rest
    except ValueError:
        title_link = title_with_link(content)
        if title_link:
            title, rest = title_link
            return title, rest
    if '.' not in content:
        # TODO: ADD OTHER ALGO
        if ' - ' in content:
            return content.split(' - ', maxsplit=1)
        return content, ''
    for maxdots in range(1, 5):
        splitted = content.split('. ', maxsplit=maxdots)
        if len(splitted) == 1:
            if invalid_title(content) == NOTITLE:
                return content, ''
        title, rest = '. '.join(splitted[:-1]), splitted[-1]
        if invalid_title(title) == NOTITLE:
            return title, rest
    return None


@utila.cacheme
def parse_hyperlinks(content):
    hyperlinks = german.hyperlink(content)
    if hyperlinks:
        for hyperlink in hyperlinks:
            content = content.replace(hyperlink, '')
    if len(hyperlinks) > 1:
        # TODO: VERIFY THIS
        utila.debug(f'more than one link parsed: {content}')
    return hyperlinks, content


@utila.cacheme
def parse_pages(content):
    parsed = german.pages(content)
    if not parsed:
        parsed = german.pages_complex(content)
    if parsed:
        content = content.replace(parsed[0], '')
    page, pageend = None, None
    if parsed:
        page = parsed[1][0]
        if len(parsed[1]) == 2:
            pageend = parsed[1][1]
    return page, pageend, content


@utila.cacheme
def parse_accessed(content):
    accessed = german.accessed(content)
    for access in accessed:
        content = content.replace(access[1], '')
    return accessed, content


def select_year(matched):
    if matched['year'] and matched['yearend']:
        year = int(matched['year'])
        yearend = int(matched['yearend'])
        return year, yearend
    if matched['year']:
        year = int(matched['year'])
        return year, None
    if matched['simpleyear']:
        year = int(matched['simpleyear'])
        return year, None
    # without year
    year: str = 'no year'
    return year, None


def select_authors(matched):
    authors: str = matched['authors']
    # backup strategy for solving typos
    authors = authors.replace(':', '.')
    authors = german.authors(authors, verbose=True)
    # decide non person authors
    authors = german.authors_decide(*authors)
    return authors


@utila.cacheme
def parse_longtext_less_strict(content: str) -> iamraw.BibliographyReference:
    for pattern in [NORMAL, BROKEN_BRACKETS]:
        parsed = parse_longtext(content, pattern=pattern)
        if not parsed:
            continue
        return parsed
    return None


TITLE_LENGTH_MIN = configo.HV_INT_PLUS(default=10)


@utila.cacheme
def title_with_link(text: str) -> str:
    """\
    >>> title_with_link('Zentrale Orte Raumordnungsprogramm (NÖ) https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    ('Zentrale Orte Raumordnungsprogramm (NÖ)', 'https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    """
    hypers = german.hyperlink(text)
    if not hypers:
        return None
    started = text.find(hypers[0])
    title = text[0:started].strip()
    rest = text[started:].strip()
    return title, rest


@utila.cacheme
def invalid_title(
    title: str,
    title_length_min: int = TITLE_LENGTH_MIN,
) -> bool:
    if not title:
        return None
    if len(title) < title_length_min:
        return True
    rate = utila.char_rate(title)
    if rate < 0.7:
        return True
    return False
