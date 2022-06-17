# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import bibliography

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'alternate',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('alternate',),
    ),
    utila.create_step(
        'column',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('column',),
    ),
    utila.create_step(
        'vspace',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('vspace',),
    ),
    utila.create_step(
        'result',
        inputs=[
            utila.ResultFile('bibliography', 'alternate_alternate'),
            utila.ResultFile('bibliography', 'column_column'),
            utila.ResultFile('bibliography', 'vspace_vspace'),
        ],
        output=('result',),
    ),
    utila.create_step(
        'legacy',
        inputs=[
            utila.ResultFile('bibliography', 'result_result'),
        ],
        output=('result',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=bibliography.ROOT,
        featurepackage='bibliography.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=bibliography.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            rename=rename,
            version=bibliography.__version__,
        ),
    )


def rename(path):
    if not isinstance(path, str):
        path = [rename(item) for item in path]
        return path
    path = utila.rreplace(
        path,
        pattern='bibliography__legacy_result',
        replace='detector__bibliography_detected',
    )
    return path
