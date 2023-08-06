import pytest
import textwrap

from ..funcs import assert_query

from ..gql import (
    FRAGMENT_PRODUCT_SHALLOW,
    FRAGMENT_PRODUCT_DEEP
)

# __________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          query Product($productId: Int) {
            product(productId: $productId) {
              ...fragmentProductDeep
            }
          }
          ''') + FRAGMENT_PRODUCT_DEEP, ],
        {'variables': {'productId': 1}},
        id='deep'
    ),
    pytest.param(
        [textwrap.dedent('''
          query Product($productId: Int) {
            product(productId: $productId) {
              ...fragmentProductDeep
            }
          }
          ''') + FRAGMENT_PRODUCT_DEEP, ],
        {'variables': {'productId': 9899}},
        id='product_id-nonexistent'
    ),
    pytest.param(
        [textwrap.dedent('''
          query ProductByTypeIdAndName($typeId: Int!, $name: String!) {
            product(typeId: $typeId, name: $name) {
              ...fragmentProductShallow
            }
          }
        ''') + FRAGMENT_PRODUCT_SHALLOW, ],
        {'variables': {'typeId': 1, 'name': "map1"}},
        id='type_id-name'
    ),
    pytest.param(
        [textwrap.dedent('''
        { product(productId: 1, name: "map1") {
            ...fragmentProductShallow
          }
        }
         ''') + FRAGMENT_PRODUCT_SHALLOW, ],
        {},
        id='product_id-name'
    ),
    pytest.param(
        [textwrap.dedent('''
        { product(productId: 1, name: "map2") {
            ...fragmentProductShallow
          }
        }
         ''') + FRAGMENT_PRODUCT_SHALLOW, ],
        {},
        id='product_id-name-nonexistent'
    ),
]

# __________________________________________________________________||


@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

# __________________________________________________________________||
