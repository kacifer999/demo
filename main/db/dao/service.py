from main.db.dao.dataset import *
from main.db.dao.image import *
from main.db.dao.task import *


def connect_db(db_dir):

    db = APSWDatabase(db_dir, pragmas={'journal_mode': 'wal',  # WAL-mode.
                                       'cache_size': 1024 * 16,
                                       'busy_timeout': 2000,
                                       'locking_mode': 'NORMAL',
                                       'synchronous': 'NORMAL'})
    DB_PROXY.initialize(db)
    db.connect(reuse_if_open=True)
    return db

def close_db(db):
    if db is None: return
    if not db.is_closed():
        db.close()
    db._conn = None
    db._state.reset()

def create_db_tables(db):
    db.create_tables([TaskModel, ImageModel, ViewModel])