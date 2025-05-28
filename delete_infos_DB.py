import sqlite3

conn = sqlite3.connect('image_predictions.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM image_predictions;")
conn.commit()

print("All records deleted.")

conn.close()
