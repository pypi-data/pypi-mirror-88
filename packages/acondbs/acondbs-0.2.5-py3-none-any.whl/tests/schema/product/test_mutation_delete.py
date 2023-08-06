import pytest

from ..funcs import assert_mutation

from ..gql import DELETE_PRODUCT

QEURY = '''
{
  allProducts {
    edges {
      node {
        name
      }
    }
  }
  allProductRelations {
    edges {
      node {
        type_ {
          name
        }
        self_ {
          name
        }
        other {
          name
        }
      }
    }
  }
  allProductFilePaths {
    edges {
      node {
        path
      }
    }
  }
}
'''


# __________________________________________________________________||
params = [
    pytest.param(
        [
            [DELETE_PRODUCT],
            {'variables': {'productId': 1}},
        ],
        [[QEURY], {}],
        id='delete'
    ),
]


@pytest.mark.parametrize('mutation, query', params)
def test_schema_success(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=True)


# __________________________________________________________________||
params = [
    pytest.param(
        [
            [DELETE_PRODUCT],
            {'variables': {'productId': 512}},
        ],
        [[QEURY], {}],
        id='error'
    ),
]


@pytest.mark.parametrize('mutation, query', params)
def test_schema_error(app, snapshot, mutation, query, mock_request_backup_db):
    assert_mutation(app, snapshot, mutation, query,
                    mock_request_backup_db, success=False)

# __________________________________________________________________||
