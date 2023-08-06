from .funcs import assert_query

##__________________________________________________________________||
def test_types(app, snapshot):

    query = '''
      {
        __schema {
          types {
            name
            description
            fields {
              name
              description
              type {
                name
              }
            }
            inputFields {
              name
              description
              defaultValue
            }
          }
        }
      }
    '''

    assert_query(app, snapshot, [[query], {}])

##__________________________________________________________________||
