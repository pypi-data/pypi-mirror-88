import pytest

from ..funcs import assert_mutation

from ..gql import CREATE_PRODUCT_TYPE

QEURY = '''
{
  allProductTypes {
    edges {
      node {
        name
      }
    }
  }
}
'''

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [CREATE_PRODUCT_TYPE],
            {'variables': {
                'input': {
                  'name': "compass",
                  'order': 5,
                  'indefArticle': "a",
                  'singular': "compass",
                  'plural': "compasses",
                  'icon': "mdi-compass"
                }
            }},
        ],
        [[QEURY], {}],
        id='create'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_success(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=True)

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [CREATE_PRODUCT_TYPE],
            {'variables': {
                'input': {
                  'name': "map",
                  'order': 5,
                  'indefArticle': "a",
                  'singular': "map",
                  'plural': "maps",
                  'icon': "mdi-map"
                }
            }},
        ],
        [[QEURY], {}],
        id='error-already-exist'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
