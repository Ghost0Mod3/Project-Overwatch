import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database/overwatch.db")


def initialize_database():
    """
    Creates the Overwatch database if it does not exist.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            summary TEXT,
            source TEXT,
            url TEXT,
            relevance INTEGER DEFAULT 0,
            category TEXT,
            created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()