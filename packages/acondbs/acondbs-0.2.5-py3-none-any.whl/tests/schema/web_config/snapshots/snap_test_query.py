# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[query] 1'] = {
    'data': {
        'webConfig': {
            'configId': '1',
            'devtoolLoadingstate': True,
            'headTitle': 'Head Title',
            'productCreationDialog': False,
            'productDeletionDialog': True,
            'productUpdateDialog': True,
            'toolbarTitle': 'Toolbar Title'
        }
    }
}
