import pytest

from ..funcs import assert_mutation

from ..gql import (
    FRAGMENT_PRODUCT_RELATION_CONNECTION,
    CREATE_PRODUCT_RELATION
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
            [CREATE_PRODUCT_RELATION],
            { 'variables': {
                'input': {
                    'typeId': 1,
                    'selfProductId': 5,
                    'otherProductId': 1
                }
            }}
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
            [CREATE_PRODUCT_RELATION],
            { 'variables': {
                'input': {
                    'typeId': 20,
                    'selfProductId': 5,
                    'otherProductId': 1
                }
            }}
        ],
        [[QEURY], {}],
        id='error-type_id-nonexistent'
    ),
    pytest.param(
        [
            [CREATE_PRODUCT_RELATION],
            { 'variables': {
                'input': {
                    'typeId': 1,
                    'selfProductId': 10,
                    'otherProductId': 1
                }
            }}
        ],
        [[QEURY], {}],
        id='error-self_product_id-nonexistent'
    ),
    pytest.param(
        [
            [CREATE_PRODUCT_RELATION],
            { 'variables': {
                'input': {
                    'typeId': 1,
                    'selfProductId': 5,
                    'otherProductId': 20
                }
            }}
        ],
        [[QEURY], {}],
        id='error-otheer_product_id-nonexistent'
    ),
    pytest.param(
        [
            [CREATE_PRODUCT_RELATION],
            { 'variables': {
                'input': {
                    'typeId': 2,
                    'selfProductId': 1,
                    'otherProductId': 4
                }
            }}
        ],
        [[QEURY], {}],
        id='error-duplicate'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
