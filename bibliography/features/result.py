# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw


def work(
    xalternate: str,
    xcolumn: str,
    xvspace: str,
) -> str:
    alternate = serializeraw.load_bibliography_reference(xalternate)
    column = serializeraw.load_bibliography_reference(xcolumn)
    vspace = serializeraw.load_bibliography_reference(xvspace)

    count_column = len(column.references)
    # alternate extracts a lot of more possible bibs, therefore we
    # have to punish the number of results. HolyValue: 0.5
    count_alternate = len(alternate.references) * 0.7
    count_vspace = len(vspace.references) * 0.5

    count_best, best = count_column, column
    for value, selected in [
        (count_alternate, alternate),
        (count_vspace, vspace),
    ]:
        if value < count_best:
            continue
        count_best = value
        best = selected
    dumped = serializeraw.dump_bibliography_reference(best)
    return dumped
