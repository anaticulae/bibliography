# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila

import bibliography.layout.vspace
import bibliography.utils


def work(  # pylint:disable=R0914
    text_oneline: str,
    textpositions_oneline: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple = None,
) -> str:
    pageslist = bibliography.utils.prepare_pages(pages)
    parts = []
    for selected in pageslist:
        textnavigators = serializeraw.ptcn_fromfile(
            text_oneline,
            textpositions_oneline,
            sizeandborder,
            headerfooter,
            pages=selected,
        )
        vspace = bibliography.layout.vspace.extracts(textnavigators)
        utila.debug(f'vspace:        {bibliography.utils.count(vspace)}')
        vspace = bibliography.judge.judge(vspace)
        utila.debug(f'vspace judged: {bibliography.utils.count(vspace)}')
        parts.append(vspace)
    # select best bib ref
    best = utila.longest(parts)
    # remove None items
    without_empty = [utila.notnone(page) for page in best]
    references = utila.flatten(without_empty)
    headline, pdfpages = None, None
    if references:
        pdfpages = tuple(sorted({item.raw_pdfpage for item in references}))
        headline = bibliography.utils.search_headline(
            text_oneline,
            textpositions_oneline,
            sizeandborder,
            headerfooter,
            page=pdfpages[0],
        )
    result = iamraw.BibliographyTable(
        headline=headline,
        references=references,
        pdfpages=pdfpages,
    )
    result.__strategy__ = 'vspace'
    # dump result
    dumped = serializeraw.dump_bibliography_reference(result)
    return dumped
