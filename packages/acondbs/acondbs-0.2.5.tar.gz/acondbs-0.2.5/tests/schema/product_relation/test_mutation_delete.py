import pytest

from ..funcs import assert_mutation

from ..gql import (
    FRAGMENT_PRODUCT_RELATION_CONNECTION,
    DELETE_PRODUCT_RELATION
    )

QEURY = '''
{
  allProductRelations {
    ...fragmentProductRelationConnection
  }
}
''' + FRAGMENT_PRODUCT_RELATION_CONNECTION

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [DELETE_PRODUCT_RELATION],
            {'variables': {'relationId': 2}},
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
            [DELETE_PRODUCT_RELATION],
            {'variables': {'relationId': 120}},
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
