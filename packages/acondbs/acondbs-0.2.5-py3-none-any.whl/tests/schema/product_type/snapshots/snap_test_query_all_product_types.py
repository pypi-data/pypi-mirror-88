# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[sort-order] 1'] = {
    'data': {
        'allProductTypes': {
            'edges': [
                {
                    'node': {
                        'icon': 'mdi-spotlight-beam',
                        'indefArticle': 'a',
                        'name': 'beam',
                        'order': 1,
                        'plural': 'beams',
                        'products': {
                            'edges': [
                            ]
                        },
                        'singular': 'beam',
                        'typeId': '2'
                    }
                },
                {
                    'node': {
                        'icon': 'mdi-map',
                        'indefArticle': 'a',
                        'name': 'map',
                        'order': 2,
                        'plural': 'maps',
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
                        'singular': 'map',
                        'typeId': '1'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[total-count] 1'] = {
    'data': {
        'allProductTypes': {
            'totalCount': 2
        }
    }
}
