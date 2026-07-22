# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import resinf
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    (hoverpower.BACHELOR037_PDF, '33:37'),
    (hoverpower.BACHELOR051_PDF, '40:52'),
    (hoverpower.BACHELOR056_PDF, '47:55'),
    (hoverpower.BACHELOR063_PDF, '59:62'),
    (hoverpower.BACHELOR075_PDF, '70:74'),
    (hoverpower.BACHELOR090_PDF, '84:90'),
    (hoverpower.BACHELOR109_PDF, '70:80'),
    (hoverpower.BACHELOR111_PDF, '70:91'),
    (hoverpower.BACHELOR128_PDF, '96:103'),
    (hoverpower.BACHELOR241_PDF, '239,240'),
    (hoverpower.BOOK173_PDF, '164:173'),
    (hoverpower.DISS143_PDF, '131:143'),
    (hoverpower.DISS148_PDF, '137:146'),
    (hoverpower.DISS167_PDF, '140:167'),
    (hoverpower.DISS170_PDF, '150:163'),
    (hoverpower.DISS172_PDF, '152:172'),
    (hoverpower.DISS178_PDF, '166:170'),
    (hoverpower.DISS205_PDF, '177,181'),
    (hoverpower.DISS266_PDF, '212:251'),
    (hoverpower.DISS272_PDF, '259:271'),
    (hoverpower.MASTER072_PDF, '65:71'),
    (hoverpower.MASTER083_PDF, '74:83'),
    (hoverpower.MASTER089_PDF, '68:82'),
    (hoverpower.MASTER091B_PDF, '82:89'),
    (hoverpower.MASTER110_PDF, '90:110'),
    (hoverpower.MASTER116_PDF, '97,98,99,100'),
    (hoverpower.MASTER148_PDF, '109:113'),
    (hoverpower.MASTER155_PDF, '78:85'),
    (hoverpower.ORDER107_PDF, '90:108'),
    resinf.todo(
        hoverpower.BACHELOR067_PDF,
        pages='63:66',
        rawmaker='--char_margin=1.1',
    ),
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER098_PDF,
]

WORKER = utilotest.worker_count(5, onci=len(RESOURCES))


def extract(resources):
    gennex.extract(
        resources,
        cleanup=True,
        footnote=True,
        pagenumber=True,
        worker=WORKER,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()
