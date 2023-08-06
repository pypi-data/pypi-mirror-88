import pytest
import textwrap

from ..funcs import assert_mutation

from ..gql import (
    FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION,
    DELETE_PRODUCT_RELATION_TYPES
    )

##__________________________________________________________________||
QEURY = '''
{
  allProductRelationTypes {
   ...fragmentProductRelationTypeConnection
  }
}
''' + FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [DELETE_PRODUCT_RELATION_TYPES],
            { 'variables': { 'typeId': 3 } }
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
            [DELETE_PRODUCT_RELATION_TYPES],
            { 'variables': { 'typeId': 512 } }
        ],
        [[QEURY], {}],
        id='error-nonexistent'
    ),
    pytest.param(
        [
            [DELETE_PRODUCT_RELATION_TYPES],
            { 'variables': { 'typeId': 1 } }
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
