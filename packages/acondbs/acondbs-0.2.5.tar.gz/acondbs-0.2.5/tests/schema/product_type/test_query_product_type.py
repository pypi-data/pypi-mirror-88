import pytest
import textwrap

from ..funcs import assert_query

from ..gql import FRAGMENT_PRODUCT_TYPE

##__________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          {
            productType(typeId: 1) {
              ...fragmentProductType
            }
          }
         ''') + FRAGMENT_PRODUCT_TYPE,],
        {},
        id='type_id'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productType(name: "map") {
              ...fragmentProductType
            }
          }
         ''') + FRAGMENT_PRODUCT_TYPE,],
        {},
        id='name'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productType(typeId: 1, name: "map") {
              ...fragmentProductType
            }
          }
         ''') + FRAGMENT_PRODUCT_TYPE,],
        {},
        id='type_id-and-name'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            productType(typeId: 2, name: "map") {
              ...fragmentProductType
            }
          }
         ''') + FRAGMENT_PRODUCT_TYPE,],
        {},
        id='type_id-and-name-nonexistent'
    ),
    pytest.param(
        ['''
          {
            productType(typeId: 1) {
              typeId
              name
              order
              indefArticle
              singular
              plural
              icon
              products(sort: DATE_PRODUCED_DESC) {
                edges {
                  node {
                    name
                  }
                }
              }
            }
          }
         ''',],
        {},
        id='type_id-sort-products'
    ),
]

##__________________________________________________________________||
@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

# __________________________________________________________________||
