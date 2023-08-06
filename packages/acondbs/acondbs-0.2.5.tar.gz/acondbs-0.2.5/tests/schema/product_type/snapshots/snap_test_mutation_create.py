# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_error[error-already-exist] 1'] = {
    'data': {
        'allProductTypes': {
            'edges': [
                {
                    'node': {
                        'name': 'map'
                    }
                },
                {
                    'node': {
                        'name': 'beam'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema_success[create] 1'] = {
    'data': {
        'createProductType': {
            'ok': True,
            'productType': {
                'icon': 'mdi-compass',
                'indefArticle': 'a',
                'name': 'compass',
                'order': 5,
                'plural': 'compasses',
                'products': {
                    'edges': [
                    ]
                },
                'singular': 'compass',
                'typeId': '3'
            }
        }
    }
}

snapshots['test_schema_success[create] 2'] = {
    'data': {
        'allProductTypes': {
            'edges': [
                {
                    'node': {
                        'name': 'map'
                    }
                },
                {
                    'node': {
                        'name': 'beam'
                    }
                },
                {
                    'node': {
                        'name': 'compass'
                    }
                }
            ]
        }
    }
}
