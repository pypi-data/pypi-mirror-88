import pytest
import textwrap

from ..funcs import assert_query

from ..gql import FRAGMENT_PRODUCT_RELATION_TYPE

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            productRelationType(typeId: 1) {
              ...fragmentProductRelationType
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_TYPE,],
        {},
        id='type_id'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productRelationType(name: "parent") {
              ...fragmentProductRelationType
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_TYPE,],
        {},
        id='name'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productRelationType(typeId: 1, name: "parent") {
              ...fragmentProductRelationType
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_TYPE,],
        {},
        id='type_id-and-name'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productRelationType(typeId: 2, name: "parent") {
              ...fragmentProductRelationType
            }
          }
        ''') + FRAGMENT_PRODUCT_RELATION_TYPE,],
        {},
        id='type_id-and-name-nonexistent)'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

# __________________________________________________________________||
