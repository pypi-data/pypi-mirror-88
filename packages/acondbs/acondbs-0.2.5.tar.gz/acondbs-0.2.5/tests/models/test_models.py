from acondbs.db.sa import sa

# __________________________________________________________________||
def test_models(app, snapshot):
    '''test the models declared
    '''
    snapshot.assert_match(sa.Model.metadata.tables)

# __________________________________________________________________||
