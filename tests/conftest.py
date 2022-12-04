# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import resinf
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(__file__)

RESOURCES = [
    (power.BACHELOR037_PDF, '33:37'),
    (power.BACHELOR051_PDF, '40:52'),
    (power.BACHELOR056_PDF, '47:55'),
    (power.BACHELOR063_PDF, '59:62'),
    (power.BACHELOR075_PDF, '70:74'),
    (power.BACHELOR090_PDF, '84:90'),
    (power.BACHELOR109_PDF, '70:80'),
    (power.BACHELOR111_PDF, '70:91'),
    (power.BACHELOR128_PDF, '96:103'),
    (power.BACHELOR241_PDF, '239,240'),
    (power.BOOK173_PDF, '164:173'),
    (power.DISS143_PDF, '131:143'),
    (power.DISS148_PDF, '137:146'),
    (power.DISS167_PDF, '140:167'),
    (power.DISS170_PDF, '150:163'),
    (power.DISS172_PDF, '152:172'),
    (power.DISS178_PDF, '166:170'),
    (power.DISS205_PDF, '177,181'),
    (power.DISS266_PDF, '212:251'),
    (power.DISS272_PDF, '259:271'),
    (power.MASTER072_PDF, '65:71'),
    (power.MASTER083_PDF, '74:83'),
    (power.MASTER089_PDF, '68:82'),
    (power.MASTER091B_PDF, '82:89'),
    (power.MASTER110_PDF, '90:110'),
    (power.MASTER116_PDF, '97,98,99,100'),
    (power.MASTER148_PDF, '109:113'),
    (power.MASTER155_PDF, '78:85'),
    (power.ORDER107_PDF, '90:108'),
    resinf.todo(
        power.BACHELOR067_PDF,
        pages='63:66',
        rawmaker='--char_margin=1.1',
    ),
    power.MASTER075_PDF,
    power.MASTER098_PDF,
]

WORKER = utilatest.worker_count(5, onci=len(RESOURCES))


def extract(resources):
    genex.extract(
        resources,
        cleanup=True,
        footnote=True,
        pagenumber=True,
        worker=WORKER,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
