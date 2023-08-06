import pytest

from ..funcs import assert_mutation

from ..gql import DELETE_PRODUCT_TYPE

QEURY = '''
{
  allProductTypes {
    edges {
      node {
        name
        typeId
      }
    }
  }
}
'''

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [DELETE_PRODUCT_TYPE],
            {'variables': { 'typeId': 2 }},
        ],
        [[QEURY], {}],
        id='delete'
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
            [DELETE_PRODUCT_TYPE],
            {'variables': { 'typeId': 12 }},
        ],
        [[QEURY], {}],
        id='error-nonexistent'
    ),
    pytest.param(
        [
            [DELETE_PRODUCT_TYPE],
            {'variables': { 'typeId': 1 }},
        ],
        [[QEURY], {}],
        id='error-unempty'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
