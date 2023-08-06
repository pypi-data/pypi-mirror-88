import pytest

from ..funcs import assert_mutation

from ..gql import (
    FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION,
    UPDATE_PRODUCT_RELATION_TYPE
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
            [UPDATE_PRODUCT_RELATION_TYPE],
            {
                'variables': {
                    'typeId': 1,
                    'input': {
                        'indefArticle': "an",
                        'singular': "mmap",
                        'plural': "mmaps"
                    },
                }}
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
            [UPDATE_PRODUCT_RELATION_TYPE],
            {
                'variables': {
                    'typeId': 1,
                    'input': {
                        'name': "mmap",
                    },
                }}
        ],
        [[QEURY], {}],
        id='error-immutable-field'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
