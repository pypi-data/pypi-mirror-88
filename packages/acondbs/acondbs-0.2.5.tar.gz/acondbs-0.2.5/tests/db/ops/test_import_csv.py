from pathlib import Path
import pytest

from acondbs import create_app
from acondbs.db.ops import define_tables
from acondbs.db.ops import import_tables_from_csv_files
from acondbs.db.ops import export_db_to_dict_of_dict_list
from acondbs.db.ops import export_db_to_csv_files

from acondbs.models import AdminAppToken

from ...constants import SAMPLE_DIR

##__________________________________________________________________||
@pytest.fixture
def app():
    config_path = Path(SAMPLE_DIR, 'config.py')
    database_uri ="sqlite:///:memory:"
    app = create_app(config_path=config_path, SQLALCHEMY_DATABASE_URI=database_uri)
    with app.app_context():
        define_tables()
    yield app


##__________________________________________________________________||
def test_non_empty(app, snapshot):
    csvdir = Path(SAMPLE_DIR, 'csv')
    with app.app_context():
        import_tables_from_csv_files(csvdir)
    with app.app_context():
        snapshot.assert_match(export_db_to_dict_of_dict_list())

##__________________________________________________________________||
def testt_empty(app, tmpdir_factory, snapshot):
    csvdir = str(tmpdir_factory.mktemp('csv'))

    with app.app_context():
        export_db_to_csv_files(csvdir)

    with app.app_context():
        import_tables_from_csv_files(csvdir)

##__________________________________________________________________||
def test_encrypted_field(app):
    csvdir = Path(SAMPLE_DIR, 'csv')
    with app.app_context():
        import_tables_from_csv_files(csvdir)
        assert 'token123' == AdminAppToken.query.one().token

def test_how_to_encrypt_and_decrypt(app, snapshot):
    unencrypted = 'token123'
    encrypted = 'aKjGknYDHY39Z2xAaN7+sQ=='

    with app.app_context():
        secret_key = app.config['SECRET_KEY'] # 'secret_key_test_123'

    from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
    engine = AesEngine()
    engine._update_key(secret_key)
    engine._set_padding_mechanism(None)

    assert engine.encrypt(unencrypted) == encrypted
    assert engine.decrypt(encrypted) == unencrypted

##__________________________________________________________________||
