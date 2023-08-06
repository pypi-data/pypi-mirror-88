import pytest
import textwrap

from ..funcs import assert_query

from ..gql import (
    FRAGMENT_PRODUCT_CONNECTION_SHALLOW,
    FRAGMENT_PRODUCT_CONNECTION_DEEP
    )

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            allProductFilePaths {
              edges {
                node {
                  pathId
                  path
                  note
                }
              }
            }
          }
        '''),],
        {},
        id='all'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProductFilePaths {
              totalCount
            }
          }
        '''),],
        {},
        id='total-count'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

##__________________________________________________________________||
