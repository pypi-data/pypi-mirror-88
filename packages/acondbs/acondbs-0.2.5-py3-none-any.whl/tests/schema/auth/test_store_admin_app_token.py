from pathlib import Path

import textwrap
from graphene.test import Client

import pytest
import unittest.mock as mock

from acondbs import create_app
from acondbs.db.ops import define_tables
from acondbs.schema.schema import create_schema
from acondbs.db.sa import sa
from acondbs.models import AdminAppToken

from ...constants import SAMPLE_DIR

##__________________________________________________________________||
STORE_ADMIN_APP_TOKEN = '''
mutation StoreAdminAppToken($code: String!) {
  storeAdminAppToken(code: $code) {
    ok
  }
}
'''

##__________________________________________________________________||
@pytest.fixture
def app():
    config_path = Path(SAMPLE_DIR, 'config.py')
    database_uri ="sqlite:///:memory:"
    app = create_app(config_path=config_path, SQLALCHEMY_DATABASE_URI=database_uri)
    with app.app_context():
        define_tables()
    yield app


##__________________________________________________________________||
@pytest.fixture(autouse=True)
def mock_githubauth(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.schema.auth.githubauth", y)
    yield y


##__________________________________________________________________||
def test_store_admin_app_token(app, mock_githubauth):

    query = STORE_ADMIN_APP_TOKEN
    variables = { 'code': 'xyz' }
    mock_githubauth.get_token.return_value = 'token0123'

    expected = {
        'storeAdminAppToken': {
            'ok': True
        }
    }

    with app.app_context():
        schema = create_schema()
        client = Client(schema)
        result = client.execute(query, variables=variables, context_value={})
        assert {'data': expected} == result

    with app.app_context():
        token = AdminAppToken.query.one()
        assert 'token0123' == token.token
        print(token.token)

def test_store_admin_app_token_update(app, mock_githubauth):

    with app.app_context():
        row = AdminAppToken(token='old_token_xyz')
        sa.session.add(row)
        sa.session.commit()

    query = STORE_ADMIN_APP_TOKEN
    variables = { 'code': 'xyz' }
    mock_githubauth.get_token.return_value = 'new_token_0123'

    expected = {
        'storeAdminAppToken': {
            'ok': True
        }
    }

    with app.app_context():
        schema = create_schema()
        client = Client(schema)
        result = client.execute(query, variables=variables, context_value={})
        assert {'data': expected} == result

    with app.app_context():
        token = AdminAppToken.query.one()
        assert 'new_token_0123' == token.token

##__________________________________________________________________||
