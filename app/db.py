import sqlite3
import os
from pathlib import Path

DB_PATH = Path(os.getenv("DATABASE_PATH", "url_shortener.db"))

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create the table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT UNIQUE NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Set the auto-increment to start at 10000
        # Only do this if the table is empty (first time setup)
        cursor.execute("SELECT COUNT(*) FROM urls")
        count = cursor.fetchone()[0]
        
        if count == 0:  # Table is empty, set starting ID
            cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('urls', 9999)")
        
        conn.commit()

# added TIMESTAMP to initial set up for optional future use (expiry time for the links)