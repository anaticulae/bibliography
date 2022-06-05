# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Reference
=========
"""

import functools
import re

import utila


@functools.lru_cache(maxsize=4098)
def years(raw: str):
    """\
    >>> years('IEEE Joint, 2004, S. 113–117')
    ('2004', 2004)
    """
    pattern = r'(?P<year>(19|20)\d{2})'
    matched = re.search(pattern, raw, re.VERBOSE)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    return (raw, int(raw))
