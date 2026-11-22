import os
import sqlite3
from typing import Generator
from contextlib import contextmanager

DB_PATH = os.environ.get("DATABASE_PATH", "/home/solomon/Desktop/ETHIOPIA-RESILIENCE-AI/resilience.db")

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db_context() -> Generator[sqlite3.Connection, None, None]:
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute_query(query: str, params: tuple = ()):
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
