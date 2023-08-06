import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables

from acondbs.db.sa import sa
from acondbs.models import ProductRelationType

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

    #
    #  +--------+                +-------+
    #  |        | --(reverse)->  |       |
    #  | parent |                | child |
    #  |        | <-(reverse)--  |       |
    #  +--------+                +-------+
    #

    #
    #  +------- -+
    #  |         | --(reverse)-+
    #  | sibling |             |
    #  |         | <-----------+
    #  +------ --+
    #

    parent = ProductRelationType(name='parent')
    child = ProductRelationType(name='child')
    parent.reverse = child
    assert child.reverse == parent

    sibling = ProductRelationType(name='sibling')
    sibling.reverse = sibling

    # commit
    with y.app_context():
        sa.session.add(parent)
        sa.session.add(sibling)
        sa.session.commit()
    yield y

# __________________________________________________________________||
def test_relations_parent_child(app):

    with app.app_context():
        parent = ProductRelationType.query.filter_by(name='parent').one_or_none()
        child = ProductRelationType.query.filter_by(name='child').one_or_none()

        assert parent is not None
        assert child is not None

        assert child is parent.reverse
        assert parent is child.reverse

def test_relations_sibling(app):

    with app.app_context():
        sibling = ProductRelationType.query.filter_by(name='sibling').one_or_none()
        assert sibling is not None
        assert sibling is sibling.reverse

def test_cascade_delete(app):

    # delete parent
    with app.app_context():
        parent = ProductRelationType.query.filter_by(name='parent').one_or_none()
        sa.session.delete(parent)
        sa.session.commit()

    # assert
    with app.app_context():
        parent = ProductRelationType.query.filter_by(name='parent').one_or_none()
        child = ProductRelationType.query.filter_by(name='child').one_or_none()

        assert parent is None
        assert child is None

# __________________________________________________________________||
