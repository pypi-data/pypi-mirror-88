# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema_success[update] 1'] = {
    'data': {
        'updateProductType': {
            'ok': True,
            'productType': {
                'icon': 'mdi-compass',
                'indefArticle': 'a',
                'name': 'map',
                'order': 5,
                'plural': 'compasses',
                'products': {
                    'edges': [
                        {
                            'node': {
                                'name': 'map1'
                            }
                        },
                        {
                            'node': {
                                'name': 'map2'
                            }
                        },
                        {
                            'node': {
                                'name': 'map3'
                            }
                        }
                    ]
                },
                'singular': 'compass',
                'typeId': '1'
            }
        }
    }
}

snapshots['test_schema_success[update] 2'] = {
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

snapshots['test_schema_error[error-nonexistent] 1'] = {
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
