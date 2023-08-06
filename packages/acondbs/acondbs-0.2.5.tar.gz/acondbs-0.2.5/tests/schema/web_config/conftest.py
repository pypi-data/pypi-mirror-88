import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables

from acondbs.db.sa import sa
from acondbs.models import (
    WebConfig
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

    c = WebConfig(
        config_id=1,
        head_title="Head Title",
        toolbar_title="Toolbar Title",
        devtool_loadingstate=True,
        product_creation_dialog=False,
        product_update_dialog=True,
        product_deletion_dialog=True
    )

    with y.app_context():
        sa.session.add(c)
        sa.session.commit()
    yield y

##__________________________________________________________________||
