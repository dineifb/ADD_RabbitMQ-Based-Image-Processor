import sqlite3


with sqlite3.connect("image_predictions.db") as conn:
    cursor = conn.cursor()
    cursor.execute('''
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
    print("✅ image_predictions table created successfully.")
