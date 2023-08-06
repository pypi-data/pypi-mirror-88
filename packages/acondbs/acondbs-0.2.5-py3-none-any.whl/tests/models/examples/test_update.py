import pytest

from acondbs.db.sa import sa
from acondbs.models import ProductType, Product

# __________________________________________________________________||
@pytest.fixture
def app(app):
    y = app

    type_map = ProductType(name='map')
    map1 = Product(name="map1", contact='xyz', type_=type_map)

    with y.app_context():
        sa.session.add(type_map)
        sa.session.commit()

    yield y

# __________________________________________________________________||
def test_simple(app):
    '''A simple test of updating an object
    '''

    with app.app_context():
        product1 = Product.query.filter_by(name='map1').first()
        assert 'xyz' == product1.contact
        product1.contact = 'abc'
        sa.session.commit()

    with app.app_context():
        product1 = Product.query.filter_by(name='map1').first()
        assert 'abc' == product1.contact

# __________________________________________________________________||
