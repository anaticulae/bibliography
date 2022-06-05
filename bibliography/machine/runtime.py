# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import pattern

import bibliography.machine.author
import bibliography.machine.title

IN = pattern.Regex(regex=r'IN:[^\*]+', name='in-pattern')

PATTERN = (
    german.issn,
    german.isbn,
    german.doi,
    german.accessed,
    german.pagenumbers,
    german.hyperlink,
    german.dates_master,
    'URL:',
    pattern.SimpleCleanup,
    IN,
    german.years,
    pattern.SimpleCleanup,
    bibliography.machine.title.Titles,
    bibliography.machine.author.SmartAuthor,
    bibliography.machine.title.TitlesBetween,
)

IMPROVES = (german.href_magic,)


def reference(raw: str) -> iamraw.BibliographyReference:
    matched = pattern.match(
        raw,
        patterns=PATTERN,
        improves=IMPROVES,
    )
    if not matched:
        return None
    data = matched['data']
    result = iamraw.BibliographyReference(raw=raw)
    authors = data.get('authors', None)
    if authors:
        result.authors = german.authors_decide(german.authors(authors))
    title = data.get('title', None)
    if title:
        if not isinstance(title, str):
            title = title[0]
        result.title = title.strip()
    hyperlink = data.get('hyperlink', None)
    if hyperlink:
        result.hyperlink = hyperlink[0][1]
    years = data.get('years')
    if years:
        result.year = int(years[0][0])
    accessed = data.get('accessed')
    if accessed:
        result.accessed = accessed[0][0]
    pagenumbers = data.get('pagenumbers')
    if pagenumbers:
        result.page, result.pageend = pagenumbers[0][0]
    publisher = data.get('in-pattern')
    if publisher:
        result.publisher = publisher[0]
    return result
