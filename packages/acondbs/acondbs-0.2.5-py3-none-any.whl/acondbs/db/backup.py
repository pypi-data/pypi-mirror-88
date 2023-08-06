"""Backup DB
"""
from pathlib import Path
import atexit
import threading
import subprocess
import warnings

from flask import current_app

from acondbs.misc.cap import cap_exec_rate
from acondbs.db.ops import export_db_to_csv_files
from acondbs.misc import gitb
from acondbs.misc import lock

##__________________________________________________________________||
def request_backup_db():
    global _lock
    global _capped_backup_func
    with _lock:
        if not _capped_backup_func:
            pause = current_app.config['ACONDBS_DB_BACKUP_CSV_GIT_PAUSE']
            _capped_backup_func = cap_exec_rate(
                func=run_flask_backup_db,
                pause_time=pause, daemon=True)
                # Need to set daemon=True. Otherwise
                # threading waits for the thread to join
                # before the function registered in atexist
                # is executed.
    _capped_backup_func()

_lock = threading.Lock()
_capped_backup_func = None

##__________________________________________________________________||
def end_backup_thread():
    global _lock
    global _capped_backup_func
    with _lock:
        if _capped_backup_func:
            _capped_backup_func.end()
        _capped_backup_func = None

import multiprocessing.queues # This import prevents the error described in
                               # https://github.com/alphatwirl/atpbar/issues/4#issuecomment-473426630

atexit.register(end_backup_thread)

##__________________________________________________________________||
def run_flask_backup_db():
    proc = subprocess.run(['flask', 'backup-db'])

##__________________________________________________________________||
def backup_db():
    repo_path = current_app.config['ACONDBS_DB_BACKUP_CSV_GIT_FOLDER']
    lock_path = current_app.config['ACONDBS_DB_BACKUP_CSV_GIT_LOCK']
    timeout = current_app.config['ACONDBS_DB_BACKUP_CSV_GIT_LOCK_TIMEOUT']
    try:
        with lock.lock(lock_path, timeout=timeout):
            backup_db_as_csv_to_github(repo_path)
    except lock.TimeOutAcquiringLock:
        warnings.warn('Time out! unable to acquire the lock in {} seconds: {}'.format(timeout, lock_path))

##__________________________________________________________________||
def backup_db_as_csv_to_github(repo_path):
    repo_path = Path(repo_path)
    for csv_file in repo_path.glob('*.csv'):
        csv_file.unlink()
    export_db_to_csv_files(repo_path)
    gitb.commit(repo_path)
    gitb.push(repo_path)

##__________________________________________________________________||
