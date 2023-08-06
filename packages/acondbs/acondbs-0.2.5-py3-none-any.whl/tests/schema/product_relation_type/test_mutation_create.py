import pytest

from ..funcs import assert_mutation

from ..gql import (
    FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION,
    CREATE_PRODUCT_RELATION_TYPES
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
            [CREATE_PRODUCT_RELATION_TYPES],
            {
                'variables': {
                    'type': {
                        'name': "doctor",
                        'indefArticle': "a",
                        'singular': "doctor",
                        'plural': "doctors"
                    },
                    'reverse': {
                        'name': "patient",
                        'indefArticle': "a",
                        'singular': "patient",
                        'plural': "patients"
                    },
                }}
        ],
        [[QEURY], {}],
        id='reverse'
    ),
    pytest.param(
        [
            [CREATE_PRODUCT_RELATION_TYPES],
            {
                'variables': {
                    'type': {
                        'name': "spouse",
                        'indefArticle': "a",
                        'singular': "spouse",
                        'plural': "spouses"
                    },
                    'selfReverse': True
                    }
            }
        ],
        [[QEURY], {}],
        id='self_reverse'
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
            [CREATE_PRODUCT_RELATION_TYPES],
            {
                'variables': {
                    'type': {
                        'name': "parent",
                        'indefArticle': "a",
                        'singular': "parent",
                        'plural': "parents"
                    },
                    'reverse': {
                        'name': "child",
                        'indefArticle': "a",
                        'singular': "child",
                        'plural': "children"
                    }
                }
            },
        ],
        [[QEURY], {}],
        id='error-already-exist'
    ),
    pytest.param(
        [
            [CREATE_PRODUCT_RELATION_TYPES],
            {
                'variables': {
                    'type': {
                        'name': "doctor",
                        'indefArticle': "a",
                        'singular': "doctor",
                        'plural': "doctors"
                    },
                    'reverse': {
                        'name': "patient",
                        'indefArticle': "a",
                        'singular': "patient",
                        'plural': "patients"
                    },
                    'selfReverse': True
                }
            }
        ],
        [[QEURY], {}],
        id='error-reverse-and-self_reverse'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

##__________________________________________________________________||
