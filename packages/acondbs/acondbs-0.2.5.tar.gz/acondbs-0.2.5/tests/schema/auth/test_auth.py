import textwrap
from graphene.test import Client

import pytest
import unittest.mock as mock

from acondbs.schema.schema import create_schema

##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mock_githubauth(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.schema.auth.githubauth", y)
    yield y


##__________________________________________________________________||
def test_auth(app, mock_githubauth):

    query = textwrap.dedent('''
        mutation GitHubAuth($code: String!) {
          githubAuth(code: $code) {
            authPayload {
              token
            }
          }
        }
    '''[1:])

    variables = { 'code': 'xyz' }

    mock_githubauth.get_token.return_value = 'token0123'

    expected = {
        'githubAuth': {
            'authPayload': {
                'token': 'token0123'
            }
        }
    }

    with app.app_context():
        schema = create_schema()
        client = Client(schema)
        result = client.execute(query, variables=variables, context_value={})
        assert {'data': expected} == result

##__________________________________________________________________||
