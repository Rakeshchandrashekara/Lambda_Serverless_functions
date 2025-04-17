# database.py
import sqlite3
from contextlib import contextmanager

def init_db():
    conn = sqlite3.connect("functions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS functions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            route TEXT NOT NULL UNIQUE,
            language TEXT NOT NULL,
            timeout INTEGER NOT NULL,
            code TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@contextmanager
def get_db():
    conn = sqlite3.connect("functions.db")
    try:
        yield conn
    finally:
        conn.close()

# Initialize database on startup
init_db()
