# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elementae
import serializeraw
import utilo


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
        headline = elementae.parse_headline(line)
        if headline is None:
            continue
        headline = headline[0]
        if not utilo.verysimilar(
                current=headline,
                expected=elementae.BIBLIOGRAPHY,
        ):
            continue
        return headline
    return None


def prepare_pages(pages) -> list:
    # analyze all pages
    pageslist = [None]
    # ensure to have connected pages
    if pages:
        pageslist = utilo.groupby_diff(pages)
    if len(pageslist) > 1:
        utilo.log(f'more than one potential bib section: {len(pageslist)}')
    return pageslist
