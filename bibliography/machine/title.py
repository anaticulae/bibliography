# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pattern
import utilo


class Titles(pattern.PatternMixin):

    QUOTATIONS = '“”'

    def __init__(self):
        super().__init__('title')

    def __call__(self, text):
        indexs = utilo.findindexs(text, Titles.QUOTATIONS)
        if not indexs:
            return []
        start, stop = min(indexs), max(indexs)
        result = text[start:stop + 1]
        return result


BETWEEN = r'(?:^\*{5,})([^*]{5,})(?:\*{5,}|$)'


class TitlesBetween(pattern.Regex):

    def __init__(self):
        """\
        >>> TitlesBetween()('********************** Hadoop YARN. ***********.')
        [' Hadoop YARN. ']
        """
        super().__init__(regex=BETWEEN, name='title')
