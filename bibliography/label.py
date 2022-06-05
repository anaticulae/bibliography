# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRefTechParser
================

Parses technical bibliographic reference like:

Technical:

.. code-block:: none

    [WL11]
    [Rum05, Seite 10]

Number:

.. code-block:: none

    [23]
    [10, Seite 10]
"""

import contextlib
import functools
import re

import iamraw
import utila

# [ ]{0,3} Optional whitespaces

PAGES = r"""
    (\,
    [ ]{0,3}(Seite|S\.)[ ]{0,3}
    (
     (?P<pagestart>\d{1,3})[ ]{0,3}\-[ ]{0,3}(?P<pageend>\d{1,3})|
     (?P<page>\d{1,3}[ ]{0,3}[f]{0,2}\.?)
    )
    ){0,1}
"""


def extract_pages(match):
    raw = utila.extract_match(match)
    page, pageend = None, None
    if match['page']:
        page, pageraw = parse_single(match['page'])  # pylint:disable=W0612
    with contextlib.suppress(KeyError, TypeError):
        page, pageend = int(match['pagestart']), int(match['pageend'])
    return page, pageend, raw


AUTHOR = r"""
    (?P<author>[\w\.]{2,4}[+]{0,1})[ ]{0,3}
    (?P<year>\d{2})[ ]{0,3}
    (?P<plus>a|b|c|d){0,1}
"""


def extract_author(match):
    plus = match['plus']
    techref = match['author'] + match['year']
    if plus is not None:
        techref += plus
    year = int(match['year'])
    year = millennium(year)
    return techref, plus, year


TECHNICAL = r"""
    \[
    [ ]{0,3}
    %s
    [ ]{0,3}
    %s
    [ ]{0,3}
    \]
""" % (AUTHOR, PAGES)

TECHNICAL_SPECIAL = r"""
    \(
        [ ]{0,3}
        \[
        [ ]{0,3}
        %s
        [ ]{0,3}
        \]
        [ ]{0,3}
        %s
        [ ]{0,3}
    \)
""" % (AUTHOR, PAGES)


@functools.lru_cache(maxsize=4096)
def parses(content: str) -> iamraw.BibliographyReferences:
    result = []
    for pattern in (TECHNICAL_SPECIAL, TECHNICAL):
        for item in re.finditer(pattern, content, re.VERBOSE):
            page, pageend, raw = extract_pages(item)
            techref, plus, year = extract_author(item)
            reference = iamraw.BibliographyReference(
                page=page,
                pageend=pageend,
                reference=techref,
                year=year,
                number=plus,
                raw=raw,
            )
            result.append(reference)
        # remove collected items
        for item in result:
            content = content.replace(item.raw, '')
    return result


NUMBER = r"""
    \[
    [ ]{0,3}
        (?P<number>\d{1,4})
    [ ]{0,3}
        %s
    [ ]{0,3}
    \]
""" % PAGES


@functools.lru_cache(maxsize=4096)
def numbers(content: str) -> iamraw.BibliographyReferences:
    result = []
    for item in re.finditer(NUMBER, content, re.VERBOSE):
        page, pageend, raw = extract_pages(item)
        number = str(item['number'])
        reference = iamraw.BibliographyReference(
            page=page,
            pageend=pageend,
            reference=number,
            raw=raw,
        )
        result.append(reference)
    return result


def parse_single(page: str):
    number = utila.parse_numbers(page)[0]
    follow = page.replace(str(number), '').strip()
    return number, follow


def millennium(year: int) -> int:
    """\
    >>> millennium(99)
    1999
    >>> millennium(0)
    2000
    >>> millennium(29)
    2029
    """
    # HINT: Works till 2030 :)
    if year < 30:
        # 2000 - 2029
        year += 2000
    else:
        # 1900 - 1999
        year += 1900
    return year
