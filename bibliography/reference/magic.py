# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Agricola, Erhard (Hrg.), Wörter und Wendungen. Wörterbuch zum deutschen.
        Sprachgebrauch, München: Max Hueber Verlag 1970.

Bergsträsser, Gotthelf, Einführung in die semitischen Sprachen, München:
        Max Hueber Verlag 1963.
"""

import german
import iamraw
import utila

YEAR = utila.compiles(r'(\d{4})\.$')


@utila.cacheme
def parse(raw: str) -> iamraw.BibliographyReference:
    """\
    >>> parse('Bergsträsser, Gotthelf, Einführung in die semitischen Sprachen, München: Max Hueber Verlag 1963.')
    BibliographyReference(title='Einführung in die semitischen Sprachen...authors=[Person(name='Bergsträsser', firstname='Gotthelf'...)
    """
    raw = raw.strip()
    rest = raw
    splitted = raw.split(',')
    # splitted: ['Bergsträsser', ' Gotthelf', ' Einführung in die
    # semitischen Sprachen', ' München: Max Hueber Verlag 1963.']
    collected = []
    for token in splitted:
        if token.strip().count(' ') <= 1:
            collected.append(token)
            continue
        if '/' in token:
            collected.append(token)
            continue
        break
    # collected: ['Bergsträsser', ' Gotthelf']
    if not collected:
        return None
    collected: str = ','.join(collected)
    authors, authors_raw = german.authors(collected, verbose=True)
    if authors == [['']]:
        # HACK: remove empty authors
        return None
    authors = german.authors_decide(authors)
    year_raw = YEAR.search(raw)
    year = int(year_raw[1]) if year_raw else None
    rest = rest.replace(authors_raw, '')
    if year_raw:
        rest = rest.replace(year_raw[0], '').strip()
    rest = rest.strip(';:, ')
    title = rest.strip() if rest.strip() else None
    if not title or not year:
        return None
    result = iamraw.BibliographyReference(
        title=title,
        authors=authors,
        year=year,
        raw=raw,
    )
    return result
