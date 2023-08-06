import pytest
import textwrap

from ..funcs import assert_query

from ..gql import FRAGMENT_PRODUCT_RELATION

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            productRelation(relationId: 1) {
              ...fragmentProductRelation
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION,],
        {},
        id='type_id'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productRelation(relationId: 222) {
              ...fragmentProductRelation
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION,],
        {},
        id='type_id-nonexistent'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

# __________________________________________________________________||
