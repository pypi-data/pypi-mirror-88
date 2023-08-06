# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_schema[app-admin] 1'] = {
    'data': {
        'oauthAppInfo': {
            'authorizeUrl': 'https://github.com/login/oauth/authorize',
            'clientId': 'client_id_admin_0123',
            'redirectUri': 'http://localhost:8080/admin/signin',
            'tokenUrl': 'https://github.com/login/oauth/access_token'
        }
    }
}

snapshots['test_schema[app] 1'] = {
    'data': {
        'oauthAppInfo': {
            'authorizeUrl': 'https://github.com/login/oauth/authorize',
            'clientId': 'client_id_0123456789',
            'redirectUri': 'http://localhost:8080/signin',
            'tokenUrl': 'https://github.com/login/oauth/access_token'
        }
    }
}
