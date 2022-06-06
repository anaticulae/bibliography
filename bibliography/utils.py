# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements
import serializeraw
import utila


def count(pages: list) -> int:
    result = [len(page) for page in pages]
    result = sum(result)
    return result


def search_headline(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    page: int = None,
) -> str:
    """Search bibliography headline to signal the user to use
    Bibliography or References.
    """
    textnavigator = serializeraw.ptcn_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        pages=page,
    )[0]
    for line in textnavigator[0:8]:
        line: str = line.text.strip()
        headline = elements.parse_headline(line)
        if headline is None:
            continue
        headline = headline[0]
        if not utila.verysimilar(
                current=headline,
                expected=elements.BIBLIOGRAPHY,
        ):
            continue
        return headline
    return None


def prepare_pages(pages) -> list:
    # analyze all pages
    pageslist = [None]
    # ensure to have connected pages
    if pages:
        pageslist = utila.groupby_diff(pages)
    if len(pageslist) > 1:
        utila.log(f'more than one potential bib section: {len(pageslist)}')
    return pageslist
