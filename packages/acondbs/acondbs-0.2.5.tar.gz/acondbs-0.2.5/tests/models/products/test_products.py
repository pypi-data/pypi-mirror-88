import pytest

from sqlalchemy import exc

from acondbs.db.sa import sa
from acondbs.models import ProductType, Product

# __________________________________________________________________||
def test_product(app_empty):
    app = app_empty

    type_map = ProductType(name='map')
    map1 = Product(name="map1", type_=type_map)

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

    with app.app_context():
        map1 = Product.query.filter_by(name='map1').one_or_none()
        assert map1 is not None
        type_map = map1.type_
        assert 'map' == type_map.name
        assert [map1] == type_map.products

# __________________________________________________________________||
def test_constraint_type_required_add(app_empty):
    app = app_empty

    map1 = Product(name="map1")

    with app.app_context():
        sa.session.add(map1)
        with pytest.raises(exc.IntegrityError):
            sa.session.commit()

    with app.app_context():
        map1 = Product.query.filter_by(name='map1').one_or_none()
        assert map1 is None

# __________________________________________________________________||
def test_constraint_type_required_delete(app_empty):
    app = app_empty

    type_map = ProductType(name='map')
    map1 = Product(name="map1", type_=type_map)

    with app.app_context():
        sa.session.add(map1)
        sa.session.commit()

    # fail to delete a type with a product
    with app.app_context():
        type_map = ProductType.query.filter_by(name='map').one_or_none()
        sa.session.delete(type_map)
        with pytest.raises(exc.IntegrityError):
            sa.session.commit()

    # assert the type and the product are still there
    with app.app_context():
        map1 = Product.query.filter_by(name='map1').one_or_none()
        assert map1 is not None
        type_map = map1.type_
        assert 'map' == type_map.name
        assert [map1] == type_map.products

    # delete the product
    with app.app_context():
        map1 = Product.query.filter_by(name='map1').one_or_none()
        sa.session.delete(map1)
        sa.session.commit()

    # assert the type still exists
    with app.app_context():
        type_map = ProductType.query.filter_by(name='map').one_or_none()
        assert type_map is not None
        assert [] == type_map.products

    # delete the type
    with app.app_context():
        type_map = ProductType.query.filter_by(name='map').one_or_none()
        sa.session.delete(type_map)
        sa.session.commit()

# __________________________________________________________________||
