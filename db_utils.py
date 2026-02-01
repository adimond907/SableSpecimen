import os
import pyodbc
from contextlib import contextmanager

# Get the database path once at module level
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "SableSpecimen_DB.accdb")
CONN_STR = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=" + DB_PATH + ";")

def get_db_connection():
    """Get a connection to the database"""
    return pyodbc.connect(CONN_STR)

@contextmanager
def db_connection():
    """Context manager for database connections - automatically closes"""
    conn = pyodbc.connect(CONN_STR)
    try:
        yield conn
    finally:
        conn.close()