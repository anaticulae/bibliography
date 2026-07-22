# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Alternate
=========

[Bra11] Braess, H.H.: Vieweg Handbuch Kraftfahrzeugtechnik. Vieweg+Teubner Verlag,
        2011 (ATZ/MTZ-Fachbuch)
[Dit13] Dittmann, D.: Alstom Hybridlokomotiven im Verschubeinsatz - Konzept und
        Erfahrungen im Einsatz H3 Fahrzeugplattform. 2013

[1] W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G.
    Teubner Stuttgart, 1994.
[2] M. Baccar, L.A. Gee, R.C. Gonzalez, and M.A. Abidi. Segmentation of
    Range Images via Data Fusion and Morphological Watersheds. Pattern
    Recognition, 29(10):1673 – 1687, 1996.
"""

import configos
import geostrat
import iamraw
import texmex
import utilo

import bibliography.reference.freeand
import bibliography.reference.magic
import bibliography.reference.number
import bibliography.reference.tech

CONTENT_LENGTH_MIN = configos.HV_INT_PLUS(default=15)

WORD_COUNT_MIN = configos.HV_INT_PLUS(default=2)

ERROR_LEVEL_MAX = configos.HV_PERCENT_PLUS(default=25.0)


def extracts(items: texmex.PTNs) -> iamraw.BibliographyReferences:
    result = []
    config = geostrat.ParserConfig(
        content_length_min=CONTENT_LENGTH_MIN,
        word_count_min=WORD_COUNT_MIN,
    )
    try:
        parsed = geostrat.al_parse_pages(items, config=config)
    except geostrat.NoMultipleLiningPoints:
        return []
    for page, navigator in zip(parsed, items):
        extracted = extract(page)
        if not extracted:
            continue
        error = len([item for item in extracted if not item])
        error_quote = error / len(extracted)
        if error_quote >= ERROR_LEVEL_MAX:
            continue
        # update pdf page number
        for item in extracted:
            item.raw_pdfpage = navigator.page
        result.append(extracted)
    return result


def extract(content) -> iamraw.BibliographyReferences:
    if content is None:
        # white page
        return []
    result = []
    for group in content:
        for line in group:
            # TODO: REMOVE THIS HACK LATER
            line.text = line.text.rstrip()
            line.text += utilo.NEWLINE
        raw = texmex.connect_text(group)
        parsed = split_bibliography(raw)
        if not parsed:
            continue
        result.append(parsed)
    return result


@utilo.cacheme
def split_bibliography(raw: str) -> iamraw.BibliographyReference:
    """\
    >>> split_bibliography('Vogel-Sprott,  M. (1997). Is behavioral  tolerance  '
    ... 'learned?  Alcohol Health & Research World, 21, 161-168.')
    BibliographyReference(...)
    >>> split_bibliography('Alaee, M. 2003. An overview of in different countries/regions and 29, 6, 683â€“689.')
    BibliographyReference(title='An overview of...)
    """
    strategies = (
        bibliography.reference.number.nosplit,
        bibliography.reference.tech.parse_single_row,
        bibliography.reference.freeand.parse_longtext_less_strict,
        bibliography.reference.tech.parse_longtext,
        bibliography.reference.magic.parse,
        parse_last,
    )
    raw = raw.strip()
    raw = utilo.simplify_chars(raw)
    splitted = bibliography.reference.number.split(raw)
    if splitted:
        raw = splitted[1]
    for strategy in strategies:
        matched = strategy(raw)
        if not matched:
            continue
        if splitted and not matched.reference:
            matched.reference = splitted[0]
        return matched
    return None


MAGIC_LENGTH_MIN = configos.HV_INT_PLUS(default=120)


@utilo.cacheme
def parse_last(raw: str) -> iamraw.BibliographyReference:
    # TODO: NOT VERY SMART
    if len(raw) < MAGIC_LENGTH_MIN:
        return None
    content = raw
    year = bibliography.reference.years(raw)
    if year:
        raw = raw.replace(year[0], '')
        year: int = year[1]
    try:
        title, rest = raw.split('-')  # pylint:disable=W0612
    except ValueError:
        title, rest = 'NO TITLE', raw
    authors = iamraw.NoPerson(raw='o.A.')
    result = iamraw.BibliographyReference(
        authors=[authors],
        title=title,
        year=utilo.int_ornone(year),
        raw=content,
    )
    return result
