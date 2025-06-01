import os
import sqlite3
import pika
import json

IMAGE_DIR = "raw_test_images"
conn = sqlite3.connect("image_predictions.db")
cursor = conn.cursor()
cursor.execute("SELECT image_name FROM image_predictions")
existing = set(row[0] for row in cursor.fetchall())
conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="raw_data")

for image_name in os.listdir(IMAGE_DIR):
    if image_name.lower().endswith((".jpg", ".jpeg", ".png")) and image_name not in existing:
        message = {
            "image_name": image_name,
            "file_path": f"{IMAGE_DIR}/{image_name}"
        }
        channel.basic_publish(
            exchange="",
            routing_key="raw_data",
            body=json.dumps(message)
        )
        print(f"[Re-Sender] Re-sent: {image_name}")

connection.close()
