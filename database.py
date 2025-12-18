import sqlite3
from flask import g

DATABASE = 'data.db'

def get_db():
    """Mengambil koneksi database yang ada atau membuat baru."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

def close_db(e=None):
    """Menutup koneksi database saat konteks aplikasi berakhir."""
    db = g.pop('_database', None)
    if db is not None:
        db.close()

def init_db():
    """Melakukan inisialisasi skema database awal."""
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        db.commit()