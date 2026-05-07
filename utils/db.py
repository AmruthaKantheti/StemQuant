import sqlite3
from config import DATABASE

def connect():
    conn=sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )
    return conn


def create_tables():

    conn=connect()
    c=conn.cursor()

    c.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
email TEXT,
password TEXT
)
""")

    c.execute("""
CREATE TABLE IF NOT EXISTS history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
sample_name TEXT,
prediction REAL,
classification TEXT,
date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

    conn.commit()
    conn.close()

create_tables()