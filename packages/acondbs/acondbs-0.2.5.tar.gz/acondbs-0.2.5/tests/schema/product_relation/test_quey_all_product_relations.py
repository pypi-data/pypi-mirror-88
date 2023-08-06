import pytest
import textwrap

from ..funcs import assert_query

from ..gql import FRAGMENT_PRODUCT_RELATION_CONNECTION

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            allProductRelations {
              ...fragmentProductRelationConnection
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_CONNECTION,],
        {},
        id='query'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProductRelations {
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

# __________________________________________________________________||
