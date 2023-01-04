# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Reference
=========
"""

import utila

YEARS = utila.compiles(r"""
    (?P<year>
        (19|20)\d{2}
    )
""")


@utila.cacheme
def years(raw: str):
    """\
    >>> years('IEEE Joint, 2004, S. 113–117')
    ('2004', 2004)
    """
    matched = YEARS.search(raw)
    if not matched:
        return None
    return (matched[0], int(matched['year']))
