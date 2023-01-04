# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def collect_quotations(text: str) -> list:
    """\
    >>> collect_quotations('N. Alsaedi, P. Burnap, „Arabic event ‘detection’ in social media“')
    [('„Arabic event ‘detection’ in social media“', 23, 65), ('‘detection’', 37, 48)]
    """
    collected = utila.findindexs(text, '„“”‘’')
    good = []
    for length in range(len(collected), 0, -1):
        for x in range(len(collected) - length):
            start, end = collected[x], collected[x + length] + 1
            quote = text[start:end]
            if count_quotation_error(quote):
                continue
            good.append((quote, start, end))
    return good


SINGLE = '‘’‚'
DOUBLE = '„“”'


def count_quotation_error(quotation, lang=None) -> int:  # pylint:disable=W0613
    failure = 0
    start, end = quotation[0], quotation[-1]
    if end == '„':
        failure += 1
    if any((
        (start in SINGLE and end in DOUBLE),
        (end in SINGLE and start in DOUBLE),
    )):
        failure += 2
    return failure


def first_quote(text: str) -> int:
    parsed = collect_quotations(text)
    if not parsed:
        return None
    first = min((item[1] for item in parsed))
    return first


def before_first_quote(text: str, starting: int = 15) -> str:
    parsed = collect_quotations(text)
    if not parsed:
        return None
    first = first_quote(text)
    if first < starting:
        return text
    return text[0:first]
