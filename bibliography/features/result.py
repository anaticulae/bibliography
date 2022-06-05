# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import bibliography.strategy


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    oneline_text: str,
    oneline_textpositions: str,
    pages: tuple = None,
) -> str:
    best = bibliography.strategy.run(
        text,
        textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        oneline_text=oneline_text,
        oneline_textpositions=oneline_textpositions,
        pages=pages,
    )
    # dump result
    dumped = serializeraw.dump_bibliography_reference(best)
    return dumped
