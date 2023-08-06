import pytest

from ..funcs import assert_mutation

from ..gql import UPDATE_PRODUCT_TYPE

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
            [UPDATE_PRODUCT_TYPE],
            {'variables': {
                'typeId': 1,
                'input': {
                  'order': 5,
                  'indefArticle': "a",
                  'singular': "compass",
                  'plural': "compasses",
                  'icon': "mdi-compass"
                }
            }},
        ],
        [[QEURY], {}],
        id='update'
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
            [UPDATE_PRODUCT_TYPE],
            {'variables': {
                'typeId': 5,
                'input': {
                  'order': 5,
                  'indefArticle': "a",
                  'singular': "compass",
                  'plural': "compasses",
                  'icon': "mdi-compass"
                }
            }},
        ],
        [[QEURY], {}],
        id='error-nonexistent'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
