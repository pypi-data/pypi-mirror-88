import pytest

from ..funcs import assert_mutation

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [
                '''
                  mutation m {
                    updateProductFilePath(pathId: 1, input: {
                      path: "nersc:/go/to/my/new_product_v2",
                      note: "- Note 1 updated",
                    }) { productFilePath { path } }
                  }
                ''',
                ],
            {}
        ],
        [
            [
                '''
                  {
                    product(productId: 1001) {
                      name datePosted producedBy note
                      paths { edges { node { path note product { productId } } } }
                    }
                  }
                ''',
            ],
            {},
        ],
        id='updateProductFilePath'
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
            [
                '''
                  mutation m {
                    updateProductFilePath(pathId: 1, input: {
                      productId: 1012
                    }) { productFilePath { path } }
                  }
                ''',
            ],
            {},
        ],
        [
            [
                '''
                  {
                    product(productId: 1001) {
                      paths { edges { node { path note product { productId } } } }
                    }
                  }
                ''',
            ],
            {},
        ],
        id='updateProductFilePath-immutableField'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

# __________________________________________________________________||
