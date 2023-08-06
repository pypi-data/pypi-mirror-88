import pytest
import textwrap

from ..funcs import assert_query

# __________________________________________________________________||
params = [
    pytest.param(
        [textwrap.dedent('''
          { webConfig {
              configId
              headTitle
              toolbarTitle
              devtoolLoadingstate
              productCreationDialog
              productUpdateDialog
              productDeletionDialog
            }
          }
          '''), ],
        {},
        id='query'
    ),
]

# __________________________________________________________________||


@pytest.mark.parametrize('args, kwags', params)
def test_schema(app, snapshot, args, kwags):
    assert_query(app, snapshot, [args, kwags])

# __________________________________________________________________||
