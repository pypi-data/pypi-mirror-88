from pathlib import Path
import warnings

import pytest
import unittest.mock as mock

from acondbs.db.backup import backup_db

##__________________________________________________________________||
@pytest.fixture()
def mock_backup_db_as_csv_to_github(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.db.backup.backup_db_as_csv_to_github", y)
    yield y

@pytest.fixture()
def mock_lock_path(app, monkeypatch, tmpdir_factory):
    folder = Path(tmpdir_factory.mktemp('backup'))
    y = folder.joinpath('lock')
    monkeypatch.setitem(app.config, 'ACONDBS_DB_BACKUP_CSV_GIT_LOCK', str(y))
    monkeypatch.setitem(app.config, 'ACONDBS_DB_BACKUP_CSV_GIT_LOCK_TIMEOUT', 0.01)
    yield y

##__________________________________________________________________||
def test_backup_db(app, mock_lock_path, mock_backup_db_as_csv_to_github):
    with app.app_context():
        repo_path = app.config['ACONDBS_DB_BACKUP_CSV_GIT_FOLDER']
        backup_db()
    assert [mock.call(repo_path)] == mock_backup_db_as_csv_to_github.call_args_list

##__________________________________________________________________||
def test_backup_db_locked(app, mock_lock_path, mock_backup_db_as_csv_to_github):
    mock_lock_path.touch()
    with app.app_context():
        with warnings.catch_warnings(record=True) as w:
            backup_db()
    assert [] == mock_backup_db_as_csv_to_github.call_args_list
    assert len(w) == 1

##__________________________________________________________________||
