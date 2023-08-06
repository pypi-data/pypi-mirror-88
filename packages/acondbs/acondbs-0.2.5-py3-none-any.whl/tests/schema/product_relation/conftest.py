import pytest

import datetime

from acondbs import create_app
from acondbs.db.ops import define_tables

from acondbs.db.sa import sa
from acondbs.models import (
    ProductType,
    Product,
    ProductFilePath,
    ProductRelationType,
    ProductRelation
    )

##__________________________________________________________________||
@pytest.fixture
def app_empty():
    database_uri ="sqlite:///:memory:"
    y = create_app(SQLALCHEMY_DATABASE_URI=database_uri)
    with y.app_context():
        define_tables()
    yield y

@pytest.fixture
def app(app_empty):

    y = app_empty

    # map1 -> beam1
    #            |
    #            +---> beam2
    #
    # map2
    # map3

    # create relation types
    Parent = ProductRelationType(type_id=1, name='parent')
    Parent.reverse = ProductRelationType(type_id=2, name='child')

    # create product types
    Map = ProductType(type_id=1, name='map')
    Beam = ProductType(type_id=2, name='beam')

    # create products
    map1 = Product(product_id=1, name="map1", date_produced=datetime.date(2020, 2, 1), type_=Map)
    map2 = Product(product_id=2, name="map2", date_produced=datetime.date(2020, 2, 10), type_=Map)
    map3 = Product(product_id=3, name="map3", date_produced=datetime.date(2020, 3, 19), type_=Map)
    beam1 = Product(product_id=4, name="beam1", date_produced=datetime.date(2020, 2, 5), type_=Beam)
    beam2 = Product(product_id=5, name="beam2", date_produced=datetime.date(2020, 3, 4), type_=Beam)

    # create relations
    relation1 = ProductRelation(relation_id=2, type_=Parent, self_=beam1, other=map1)
    relation2 = ProductRelation(relation_id=4, type_=Parent, self_=beam2, other=beam1)

    with y.app_context():
        sa.session.add(Map)
        sa.session.add(Beam)
        sa.session.commit()
    yield y

##__________________________________________________________________||
