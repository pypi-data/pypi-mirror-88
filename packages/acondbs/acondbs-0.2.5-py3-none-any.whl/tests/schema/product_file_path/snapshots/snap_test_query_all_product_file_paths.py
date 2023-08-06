# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[all] 1'] = {
    'data': {
        'allProductFilePaths': {
            'edges': [
                {
                    'node': {
                        'note': '',
                        'path': 'nersc:/go/to/my/maps',
                        'pathId': '1'
                    }
                },
                {
                    'node': {
                        'note': 'lat only',
                        'path': 'nersc:/go/to/my/maps_v2',
                        'pathId': '2'
                    }
                },
                {
                    'node': {
                        'note': 'lat only',
                        'path': 'abcde:/path/to/the/maps_v2',
                        'pathId': '3'
                    }
                },
                {
                    'node': {
                        'note': 'lat only',
                        'path': 'nersc:/go/to/my/maps_v3',
                        'pathId': '4'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'BEAM_DEPOT/Beams/20190304',
                        'pathId': '5'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'BEAM_DEPOT/Beams/20190607',
                        'pathId': '6'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'BEAM_DEPOT/Beams/20200123',
                        'pathId': '7'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'BEAM_DEPOT/Beams/20200207',
                        'pathId': '8'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'nersc:/go/to/my/simulations',
                        'pathId': '9'
                    }
                },
                {
                    'node': {
                        'note': '',
                        'path': 'abcde:/path/to/the/simulations',
                        'pathId': '10'
                    }
                }
            ]
        }
    }
}

snapshots['test_schema[total-count] 1'] = {
    'data': {
        'allProductFilePaths': {
            'totalCount': 10
        }
    }
}
