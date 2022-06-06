# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""VSPACE
======

Global vs Local Optimization
----------------------------

1. Run equal text line distance optimization
2. TODO: Merge to a single navigator and run optimization
3. Run separate optimization for every single page

"""

import typing

import configo
import iamraw
import texmex
import utila

import bibliography.judge
import bibliography.layout.alternate
import bibliography.layout.utils


def extracts(
    navigators: texmex.PageTextContentNavigator
) -> iamraw.BibliographyReferences:
    glob = optimize_global(navigators)
    return glob


def optimize_global(
    navigators: texmex.PageTextContentNavigator
) -> iamraw.BibliographyReferences:
    results = []
    for factor in MAXDISTANCE_FACTOR:
        adjusted = lambda x: factor * MAXDISTANCE(x)  # pylint:disable=cell-var-from-loop
        current = []
        for navigator in navigators:
            extracted = extract(navigator, vspace_max=adjusted)
            current.extend(extracted)
        results.append(current)
    best = select_best(results)
    result = groupby_x(best, lambda x: x.raw_pdfpage)
    return result


def extract(
    navigator: texmex.NavigatorMixin,
    vspace_max: callable = None,
) -> iamraw.BibliographyReferences:
    if vspace_max is None:
        vspace_max = MAXDISTANCE
    grouped = texmex.group_linedistances_complex(
        navigator,
        distance_max=vspace_max,
    )
    grouped = [[navigator[item] for item in group] for group in grouped]
    result = bibliography.layout.alternate.extract(grouped)
    result = utila.not_none(result)
    # update pdf page number
    for item in result:
        item.raw_pdfpage = navigator.page
    return result


MAXDISTANCE = configo.HolyTable(
    items=[
        (12.0, 15.0),  # LOWER LIMIT
        (14.5, 30.0),
        (15.96, 35),
        (60.0, 50.0),  # UPPER LIMIT
    ],
    strategy=utila.Strategy.LOWER,
)

MAXDISTANCE_FACTOR = configo.HolyList([
    0.8,
    0.85,
    0.90,
    0.95,
    1.0,
    1.05,
    1.1,
    1.5,
    1.7,
    2.0,
    2.3,
    2.6,
])


def select_best(items: list, selector=len) -> typing.Any:
    # count valid items only
    items = [
        item for item in items if bibliography.judge.judge([item]) and
        not bibliography.layout.utils.invalid_extraction(item)
    ]
    # TODO: REPLACE WITH UTILA CODE
    if not items:
        return []
    best = items[0]
    for item in items[1:]:
        if selector(item) < selector(best):
            continue
        best = item
    return best


def groupby_x(items, selector):
    # TODO: MOVE TO UTILA
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        if selector(result[-1][0]) == selector(item):
            result[-1].append(item)
        else:
            result.append([item])
    return result
