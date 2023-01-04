# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def invalid_extraction(result) -> bool:
    if invalid_title(result):
        return True
    if invalid_year(result):
        return True
    return False


def invalid_title(result) -> bool:
    if not result:
        return False
    notitle = len([item for item in result if not item.title])
    rate = notitle / len(result)
    if rate > 0.1:
        return True
    return False


def invalid_year(result) -> bool:
    noyear = len([item for item in result if not item.year])
    rate = noyear / len(result)
    if rate > 0.1:
        return True
    return False
