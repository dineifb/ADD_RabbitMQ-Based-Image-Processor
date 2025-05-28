import pika
import json
import os

# Path to test image directory (adjust this!)
TEST_DIR = "raw_test_images"  # e.g., "data/test"

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='raw_data')

# Get all image files from the directory
image_files = [f for f in os.listdir(TEST_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for image_name in image_files:
    file_path = os.path.abspath(os.path.join(TEST_DIR, image_name))
    
    data = {
        "image_name": image_name,
        "file_path": file_path
    }

    # Send to RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='raw_data',
        body=json.dumps(data)
    )
    print(f"[Producer] Sent: {data}")

connection.close()