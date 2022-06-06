# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import texmex
import utila

import bibliography.judge
import bibliography.layout.alternate
import bibliography.layout.column
import bibliography.layout.vspace
import bibliography.utils


def run(  # pylint:disable=R0914
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    oneline_text: str,
    oneline_textpositions: str,
    pages: tuple = None,
) -> iamraw.BibliographyTable:
    pageslist = bibliography.utils.prepare_pages(pages)
    parts = []
    for selected in pageslist:
        textnavigators = serializeraw.ptcn_fromfile(
            text,
            textpositions,
            sizeandborder,
            headerfooter,
            pages=selected,
        )
        onelines = serializeraw.ptcn_fromfile(
            oneline_text,
            oneline_textpositions,
            sizeandborder,
            headerfooter,
            pages=selected,
        )
        extracted = extracts(
            textnavigators,
            onelines,
        )
        parts.append(extracted)
    # select best bib ref
    best = utila.longest(parts, key=lambda x: x[0])
    # remove None items
    without_empty = [utila.notnone(page) for page in best[0]]
    references = utila.flatten(without_empty)
    headline, pdfpages = None, None
    if references:
        pdfpages = tuple(sorted({item.raw_pdfpage for item in references}))
        headline = bibliography.utils.search_headline(
            oneline_text,
            oneline_textpositions,
            sizeandborder,
            headerfooter,
            page=pdfpages[0],
        )
    result = iamraw.BibliographyTable(
        headline=headline,
        references=references,
        pdfpages=pdfpages,
    )
    result.__strategy__ = best[1]
    return result


def extracts(
    text: texmex.PageTextNavigators,
    text_oneline: texmex.PageTextNavigators,
) -> iamraw.BibliographyReferences:
    column = bibliography.layout.column.extracts(text)
    alternate = bibliography.layout.alternate.extracts(text_oneline)
    vspace = bibliography.layout.vspace.extracts(text_oneline)
    # print result of un-judged extraction
    utila.debug('judge data')
    utila.debug(f'column:    {bibliography.utils.count(column)}')
    utila.debug(f'alternate: {bibliography.utils.count(alternate)}')
    utila.debug(f'vspace:    {bibliography.utils.count(vspace)}')
    utila.debug()
    # column = bibliography.judge.judge(column)
    alternate = bibliography.judge.judge(alternate)
    vspace = bibliography.judge.judge(vspace)
    # print judge result
    utila.debug('judged')
    utila.debug(f'column:    {bibliography.utils.count(column)}')
    utila.debug(f'alternate: {bibliography.utils.count(alternate)}')
    utila.debug(f'vspace:    {bibliography.utils.count(vspace)}')

    count_column = bibliography.utils.count(column)
    # alternate extracts a lot of more possible bibs, therefore we
    # have to punish the number of results. HolyValue: 0.5
    count_alternate = bibliography.utils.count(alternate) * 0.7
    count_vspace = bibliography.utils.count(vspace) * 0.5

    count_best, best, best_strategy = count_column, column, 'column'
    for value, selected, strategy in [
        (count_alternate, alternate, 'alternate'),
        (count_vspace, vspace, 'vspace'),
    ]:
        if value < count_best:
            continue
        count_best = value
        best = selected
        best_strategy = strategy
    return best, best_strategy
