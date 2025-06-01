import pika
import os
import json

IMAGE_DIR = "raw_test_images"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='raw_data')

for image_name in os.listdir(IMAGE_DIR):
    if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        message = {
            "image_name": image_name.strip().lower(),
            "file_path": f"{IMAGE_DIR}/{image_name}"
        }
        channel.basic_publish(
            exchange='',
            routing_key='raw_data',
            body=json.dumps(message)
        )
        print(f"[Producer] Sent metadata for: {image_name}")

connection.close()
