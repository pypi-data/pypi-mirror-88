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
            allProducts {
              ...fragmentProductConnectionDeep
            }
          }
        ''') + FRAGMENT_PRODUCT_CONNECTION_DEEP,],
        {},
        id='deep'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(first: 2) {
              ...fragmentProductConnectionShallow
            }
          }
        ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='first-two'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(first: 2, sort: DATE_PRODUCED_DESC) {
              ...fragmentProductConnectionShallow
            }
          }
         ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='first-two-sort'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(filters: {typeId: 1}, first: 2) {
              ...fragmentProductConnectionShallow
            }
          }
         ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='filters-type_id-first-two'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(filters: {typeName: "map"}, first: 2) {
              ...fragmentProductConnectionShallow
            }
          }
         ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='filters-type_name-first-two'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(filters: {typeId: 1}, sort: DATE_PRODUCED_DESC) {
              ...fragmentProductConnectionShallow
            }
          }
         ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='filters-type_id-sort'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(filters: {typeName: "map"}, sort: DATE_PRODUCED_DESC) {
              ...fragmentProductConnectionShallow
            }
          }
         ''') + FRAGMENT_PRODUCT_CONNECTION_SHALLOW,],
        {},
        id='filters-type_name-sort'
    ),
    pytest.param(
        [textwrap.dedent('''
          {
            allProducts(filters: {typeName: "map"}, first: 2) {
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
