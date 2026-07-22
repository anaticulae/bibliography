# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import iamraw
import texmex
import utilo

import bibliography.layout.vspace
import bibliography.machine.runtime


def extracts(navigators: texmex.PTNs):
    for strategy in (extract, double_column):
        result = []
        for navigator in navigators:
            extracted = strategy(navigator)
            if not extracted:
                continue
            # update pdf page number
            for item in extracted:
                item.raw_pdfpage = navigator.page
            result.append(extracted)
        if result:
            return result
    return []


def extract(content: texmex.PTN) -> iamraw.BibliographyReferences:
    layouted = geostrat.parse(
        content,
        column_elements_min=4,
        data_adjust=True,
    )
    if layouted is None:
        return None
    result = []
    for left, right in layouted:
        if not left:
            # TODO: INVESTIGATE WHY THIS CAN HAPPEN, SEE DISS264
            continue
        reference = left[0].text.strip()
        if reference[0] != '[':
            # TODO: VALIDATE PATTERN
            continue
        # remove latex reference pattern [FCB87]
        raw = ' '.join(item.text.strip() for item in right)
        if not raw.strip():
            # no content in data column
            continue
        parsed = bibliography.machine.runtime.reference(raw)
        parsed.reference = reference
        result.append(parsed)
    return result


def double_column(content: texmex.PTN) -> iamraw.BibliographyReferences: # yapf:disable
    parsed = geostrat.parse(content, column_count=2)
    if parsed is None:
        return None
    result = []
    for column in parsed:
        navigator = texmex.PTN()
        navigator.data = column
        parsed = bibliography.layout.vspace.extracts([navigator])
        result.extend(utilo.flat(parsed))
    return result
