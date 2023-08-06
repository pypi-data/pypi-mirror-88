import pytest

from ..funcs import assert_mutation

##__________________________________________________________________||
params = [
    pytest.param(
        [
            [
                '''
                  mutation m {
                    createProductFilePath(input: {
                      path: "nersc:/go/to/my/new_product_v1",
                      note: "- Note 1",
                      productId: 1010
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
                    product(productId: 1010) {
                      name datePosted producedBy note
                      paths { edges { node { path note product { productId } } } }
                    }
                  }
                ''',
            ],
            {},
        ],
        id='createProductFilePath'
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
                    createProductFilePath(input: {
                      path: "nersc:/go/to/my/new_product_v1",
                      note: "- Note 1",
                      productId: 1010,
                      noSuchField: "xxx"
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
                    allProductFilePaths {
                      edges {
                        node {
                          productId
                        }
                      }
                    }
                  }
                ''',
            ],
            {},
        ],
        id='createProductFilePath-noSuchField'
    ),
]

@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

# __________________________________________________________________||
