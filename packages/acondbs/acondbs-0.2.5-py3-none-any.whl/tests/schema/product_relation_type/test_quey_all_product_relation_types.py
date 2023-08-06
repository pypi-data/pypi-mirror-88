import pytest
import textwrap

from ..funcs import assert_query

from ..gql import FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            allProductRelationTypes {
              ...fragmentProductRelationTypeConnection
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION,],
        {},
        id='query'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProductRelationTypes {
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
