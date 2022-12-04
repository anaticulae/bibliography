# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import bibliography.utils

TITLE_LENGTH_MIN = configo.HV_INT_PLUS(default=10)

INVALID_MAX = configo.HolyTable(items=[
    (5, 0),
    (15, 0),
    (30, 3 / 30),
    (100, 10 / 100),
])


def judge(pages: list) -> list:
    counted = bibliography.utils.count(pages)
    if not counted:
        return []
    invalid = 0
    for item in utila.flat(pages):
        if item is None or invalid_single(item):
            invalid += 1
    # determine invalid ratio
    ratio = invalid / counted
    # use greater instead of greater equal to pass zero findings with
    # ration 0.0 and allowed ratio of 0.0
    if ratio > INVALID_MAX(counted):
        # invalid result
        return []
    return pages


def invalid_single(
    item: iamraw.BibliographyReference,
    title_length_min: int = TITLE_LENGTH_MIN,
) -> bool:
    if item.reference:
        # if reference is detected this is a sign for good extraction
        # TODO: VALIDATE REFERENCE HERE?
        return False
    if item.title:
        if len(item.title) < title_length_min:
            return True
    return False
