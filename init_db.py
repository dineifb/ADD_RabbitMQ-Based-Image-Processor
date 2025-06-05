import sqlite3
import os


DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "image_predictions.db")

with sqlite3.connect(DB_PATH) as conn:
    conn.execute("PRAGMA journal_mode=WAL;")  # 👈 Add this line
    conn.execute('''
        CREATE TABLE IF NOT EXISTS image_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_name TEXT UNIQUE,
            file_path TEXT,
            prediction TEXT,
            confidence REAL,
            processed_at TIMESTAMP
        )
    ''')
    conn.commit()

print("✅ SQLite DB initialized with WAL mode")
