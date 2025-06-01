# resend_unprocessed.py
import os
import sqlite3
import pika
import json

IMAGE_DIR = "raw_test_images"
conn = sqlite3.connect("image_predictions.db")
cursor = conn.cursor()
cursor.execute("SELECT image_name, prediction FROM image_predictions")
unprocessed = [row[0] for row in cursor.fetchall() if row[1] is None]
conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="raw_data")

for image_name in unprocessed:
    file_path = os.path.join(IMAGE_DIR, image_name)
    if os.path.exists(file_path):
        msg = {"image_name": image_name, "file_path": file_path}
        channel.basic_publish(exchange="", routing_key="raw_data", body=json.dumps(msg))
        print(f"[Re-Sent] {image_name}")

connection.close()
