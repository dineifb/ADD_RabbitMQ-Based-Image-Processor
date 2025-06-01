import sqlite3
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "image_predictions.db")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Query to select all records
cursor.execute("SELECT * FROM image_predictions")

# Fetch all rows
rows = cursor.fetchall()

# Print column names
print(f"{'ID':<5} {'Image Name':<20} {'File Path':<40} {'Prediction':<10} {'Confidence':<10} {'Processed At'}")
print('-' * 100)

# Print each row in a readable format
for row in rows:
    id, image_name, file_path, prediction, confidence, processed_at = row
    print(f"{id:<5} {image_name:<20} {file_path:<40} {prediction or '-':<10} {confidence or '-':<10} {processed_at}")

conn.close()
