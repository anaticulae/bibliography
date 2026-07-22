# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import bibliography

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'alternate',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
        ],
        output=('alternate',),
    ),
    utilo.create_step(
        'column',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
        ],
        output=('column',),
    ),
    utilo.create_step(
        'vspace',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('footnote', 'result_result'),
        ],
        output=('vspace',),
    ),
    utilo.create_step(
        'result',
        inputs=[
            utilo.ResultFile('bibliography', 'alternate_alternate'),
            utilo.ResultFile('bibliography', 'column_column'),
            utilo.ResultFile('bibliography', 'vspace_vspace'),
        ],
        output=('result',),
    ),
    utilo.create_step(
        'legacy',
        inputs=[
            utilo.ResultFile('bibliography', 'result_result'),
        ],
        output=('result',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=bibliography.ROOT,
        featurepackage='bibliography.features',
        config=utilo.FeaturePackConfig(
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
    path = utilo.rreplace(
        path,
        pattern='bibliography__legacy_result',
        replace='detector__bibliography_detected',
    )
    return path
