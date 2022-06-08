# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> parse_longtext('JOHNSON, Bobbie (11.1.2010): Privacy no longer a social '
... 'norm, says Facebook founder. http://www.theguardian.com/technology/2010'
... '/jan/11/facebook-privacy (Stand: 15.7.2014). ')
BibliographyReference(title='Privacy no longer a social norm, says Facebook founder'...)
"""

import german
import iamraw
import utila

import bibliography.label
import bibliography.quotes
import bibliography.reference
import bibliography.reference.freeand


@utila.cacheme
def parse_single_row(content: str) -> iamraw.BibliographyReference:
    matched = bibliography.label.parses(content)
    if not matched:
        matched = bibliography.label.numbers(content)
    if not matched:
        return None
    if len(matched) > 1:
        # Mostly a result of failure in layout grouping. This can
        # happen if a wrong layout grouping mechanism is used. This is not
        # a problem cause we have more than one strategy.
        # utila.debug('parses more than one reference, '
        #             f'skip tech result: {content}')
        return None
    matched: iamraw.BibliographyReference = matched[0]
    content = content.replace(matched.raw, '').strip()
    detected = bibliography.reference.tech.parse_longtext(content)
    if not detected:
        # no further information detected
        return matched
    # append information of second parsing step
    matched.title = detected.title
    matched.authors = detected.authors
    matched.publisher = detected.publisher
    matched.raw += detected.raw
    return matched


def ghost_strip(text, pattern, count: int = 1):
    text = text.replace(pattern, '*' * len(pattern), count)
    return text


@utila.cacheme
def parse_longtext(content: str) -> iamraw.BibliographyReference:
    """\
    >>> parse_longtext('Todd D. Jick. “Mixing Qualitative and Quantitative '
    ... 'Methods: Triangulation in Action.” In: AdministrativeScienceQuarterly '
    ... '24 (1979), pp. 602– 611.')
    BibliographyReference(title='“Mixing...authors=[Person(name='Todd', firstname='D. Jick.'...raw_pdfpage=None)
    >>> parse_longtext('Koch, Stefan (Hg.) (2008): Customer & supplier '
    ... 'relationship management. Beziehungsmanagement ;')
    BibliographyReference(title='Customer & supplier relationship management'...year=2008...)
    >>> parse_longtext('HORNIG, Frank (17.7.2006): Du bist das Netz! '
    ... 'http://www.spiegel.de/spiegel/print/d47602985.html (Stand: 15.7.2014).')
    BibliographyReference(title='Du bist das Netz!  (Stand: 15',...authors=[Person(...raw='HORNIG Frank')]...)
    """
    content = utila.normalize_text(content)
    raw = content
    parsed = parse_first(content)
    if not parsed:
        return None
    authors, rest = parsed
    access, rest = bibliography.reference.freeand.parse_accessed(rest)
    # hyperlink is a very strong pattern
    hyperlinks, rest = bibliography.reference.freeand.parse_hyperlinks(rest)
    year, rest = parse_year(rest)
    try:
        title, rest = parse_title(rest)
    except TypeError:
        return None
    title = title.strip(' :,;')
    authors = authors.strip()
    authors = german.authors(authors)
    # disable non person authors
    authors = german.authors_decide(authors)
    page = german.pages(rest)
    if page:
        rest = ghost_strip(rest, page[0])
    # TODO: ADD PUBLISHER EXTRACTOR
    rest = rest.strip()
    publisher = parse_publisher(rest)
    result = iamraw.BibliographyReference(
        authors=authors,
        title=title,
        publisher=publisher,
        hyperlink=hyperlinks,
        accessed=access,
        year=year,
        raw=raw,
    )
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]
    return result


def parse_year(text: str) -> tuple:
    """\
    >>> parse_year('(2008): Customer & supplier')
    (2008, 'Customer & supplier')
    >>> parse_year('(2013): Columbia Newsblaster: ')
    (2013, 'Columbia Newsblaster')
    >>> parse_year('(17.7.2006): Du bist das Netz! http://www.spiegel.de/'
    ... 'spiegel/print/d47602985.html (Stand: 15.7.2014).')
    (2006, 'Du bist das Netz! http://www.spiegel.de/...html (Stand: 15.7.2014).')
    >>> parse_year('2003. An overview of commercially')
    (2003, 'An overview of commercially')
    """
    # 1. Try to detect complex date
    dates = german.dates_master(text, verbose=True, sort=False)
    if dates:
        year_first = dates[0][1], dates[0][0][0]
    else:
        year_first = None
    year_second = bibliography.reference.years(text)
    if year_first and year_second:
        if text.find(year_first[0]) <= text.find(year_second[0]):
            year = year_first
        else:
            year = year_second
    elif year_first:
        year = year_first
    else:
        year = year_second
    if year is None:
        return None, text
    # remove year from right to left
    pattern = f'({year[0]})'
    text = text.replace(pattern, '')
    text = text.replace(f'{year[0]}.', '')
    # remove fragment from year splitter, TODO: remove later!
    text = text.replace('( )', '').strip()
    text = text.replace('()', '').strip()
    text = text.strip(':,; ')
    return int(year[1]), text


FIRST_SPLIT = utila.compiles(r"""
(
    \((19|20)\d{2}\)|                    # year
    (19\d{2}|20[012]\d)\.|               # year.
    \((\d{1,4}\.\d{1,2}\.\d{1,4})\)\:?|  # date
    (https|http)\:|
    \:
)
""")


@utila.cacheme
def parse_first(content: str):
    """\
    >>> parse_first('Put People First. http://www.putpeoplefirst.org.uk/ (19.1.2015).')
    ('Put People First. ', 'http://www.putpeoplefirst.org.uk/ (19.1.2015).')
    >>> parse_first('Koch, Stefan (Hg.) (2008): Customer a little bit longer')
    ('Koch, Stefan (Hg.) ', '(2008): Customer a little bit longer')
    >>> parse_first('HORNIG, Frank (17.7.2006): Du bist das Netz! ')
    ('HORNIG, Frank ', '(17.7.2006): Du bist das Netz! ')
    """
    authors = bibliography.quotes.before_first_quote(content, starting=5)
    if authors:
        if len(authors) <= content.find(':'):
            # quote starts before first collon
            rest = content.replace(authors, '')
            return authors, rest
    detected = FIRST_SPLIT.search(content)
    if not detected:
        return None
    authors, rest = content[:detected.start()], content[detected.start():]
    rest = rest[1:] if rest[0] == ':' else rest
    if len(authors) > 160:  # TODO: HOLY VALUE
        # WAY TO LONG
        return None
    if not rest or len(rest) < 30:
        return None
    return authors, rest


@utila.cacheme
def parse_title(rest: str) -> tuple:
    rest = rest.strip()
    if rest.find('.') > 20:  # TODO: TITLE MIN LENGTH
        return rest.split('.', maxsplit=1)
    if ';' in rest:
        return rest.split(';', maxsplit=1)
    if ',' in rest:
        return rest.split(',', maxsplit=1)
    return None


@utila.cacheme
def parse_publisher(rest: str):
    if not rest:
        return None
    rest = rest.strip()
    if len(rest) < 10:
        # Not a valid publisher
        return None
    return rest
