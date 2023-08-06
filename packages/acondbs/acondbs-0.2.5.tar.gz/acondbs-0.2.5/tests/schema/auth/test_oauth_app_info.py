import pytest

from ..funcs import assert_query

OAUTH_APP_INFO = '''
query OauthAppInfo($admin: Boolean) {
  oauthAppInfo(admin: $admin) {
    clientId
    authorizeUrl
    tokenUrl
    redirectUri
  }
}
'''

##__________________________________________________________________||
params = [
    pytest.param(
        [OAUTH_APP_INFO],
        {'variables': {'admin': False}},
        id='app'
    ),
    pytest.param(
        [OAUTH_APP_INFO],
        {'variables': {'admin': True}},
        id='app-admin'
    )
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

##__________________________________________________________________||
