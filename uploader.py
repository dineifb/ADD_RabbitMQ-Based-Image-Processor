import pika
import json
import sqlite3
import threading

# Connect to SQLite DB
conn = sqlite3.connect('image_predictions.db', check_same_thread=False)
cursor = conn.cursor()

# Function to handle raw image metadata from Producer
def handle_raw_data(ch, method, properties, body):
    data = json.loads(body)
    image_name = data.get('image_name')
    file_path = data.get('file_path')

    print(f"[Uploader] Received raw image data: {data}")

    try:
        cursor.execute(
            '''
            INSERT INTO image_predictions (image_name, file_path)
            VALUES (?, ?)
            ''',
            (image_name, file_path)
        )
        conn.commit()
        print(f"[Uploader] Inserted image {image_name}")
    except sqlite3.IntegrityError:
        print(f"[Uploader] Image {image_name} already exists. Skipping.")

# Function to handle processed results from Processor
def handle_processed_data(ch, method, properties, body):
    data = json.loads(body)
    image_name = data.get('image_name')
    prediction = data.get('prediction')
    confidence = data.get('confidence')

    print(f"[Uploader] Received processed data: {data}")

    cursor.execute(
        '''
        UPDATE image_predictions
        SET prediction = ?, confidence = ?, processed_at = CURRENT_TIMESTAMP
        WHERE image_name = ?
        ''',
        (prediction, confidence, image_name)
    )
    conn.commit()
    print(f"[Uploader] Updated prediction for {image_name}")

# Setup for raw_data queue
def consume_raw_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='raw_data')
    channel.basic_consume(queue='raw_data', on_message_callback=handle_raw_data, auto_ack=True)
    print("[Uploader] Waiting for raw_data...")
    channel.start_consuming()

# Setup for processed_data queue
def consume_processed_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='processed_data')
    channel.basic_consume(queue='processed_data', on_message_callback=handle_processed_data, auto_ack=True)
    print("[Uploader] Waiting for processed_data...")
    channel.start_consuming()

# Run both consumers in separate threads
threading.Thread(target=consume_raw_data).start()
threading.Thread(target=consume_processed_data).start()
