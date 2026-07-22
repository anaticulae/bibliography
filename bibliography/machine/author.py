# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import germania
import pattern
import utilo

VALIDS = 'u.a. and und & et.al.'.split()


class SmartAuthor(pattern.PatternMixin):

    def __init__(self):
        super().__init__('authors')

    def __call__(self, text):
        return collect(text)


def collect(text: str) -> str:
    """\
    >>> collect('Michael Bevilacqua-Linn. Functional Programming Patterns in Scala and Clojure.*')
    'Michael Bevilacqua-Linn.'
    """
    first_star = text.find('*')
    if first_star != -1:
        text = text[0:first_star]
    authors = till_valid(text)
    return authors


NAME = utilo.compiles(r'\w{1,3}\.')


def till_valid(text: str, error_max: int = 1):
    """\
    >>> till_valid('Michael Bevilacqua-Linn. Functional Programming Patterns in Scala')
    'Michael Bevilacqua-Linn.'
    """
    words = text.split()
    valid = [
        germania.isperson(item) or item in VALIDS or NAME.match(item)
        for item in words
    ]
    valid = gap_max(valid, bridge=error_max)
    joined = ' '.join(words[0:len(valid)])
    return joined


def gap_max(items: list, bridge: int = 1) -> list:
    result = []
    error = 0
    for item in items:
        if item:
            error = 0
            result.append(item)
            continue
        if not item:
            error += 1
        if error > bridge:
            break
        result.append(item)
    while result and not result[-1]:
        # remove errors at end
        result.pop()
    return result
