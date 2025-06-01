import pika
import json
import sqlite3
import threading
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "image_predictions.db")

def handle_raw_data(ch, method, properties, body):
    print("[Uploader] Using DB path:", os.path.abspath("image_predictions.db"))
        
    data = json.loads(body)
    image_name = data.get('image_name').strip().lower()
    file_path = data.get('file_path')

    print(f"[Uploader] Received raw image data: {data}")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
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
    except Exception as e:
        print(f"[Uploader] Error inserting image {image_name}: {e}")

def handle_processed_data(ch, method, properties, body):
    data = json.loads(body)
    image_name = data.get('image_name').strip().lower()
    prediction = data.get('prediction')
    confidence = data.get('confidence')

    print(f"[Uploader] Received processed data: {data}")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT image_name FROM image_predictions WHERE image_name = ?", (image_name,))
            found = cursor.fetchone()
            print(f"[Uploader] DB match result for '{image_name}': {found}")


            # Log exact match query
            cursor.execute("SELECT COUNT(*) FROM image_predictions WHERE lower(image_name) = ?", (image_name,))
            count = cursor.fetchone()[0]
            print(f"[Uploader] Entries found for '{image_name}': {count}")

            # Run update
            cursor.execute(
                '''
                UPDATE image_predictions
                SET prediction = ?, confidence = ?, processed_at = CURRENT_TIMESTAMP
                WHERE image_name = ?
                ''',
                (prediction, confidence, image_name)
            )
            conn.commit()
            print(f"[Uploader] Rows updated: {cursor.rowcount}")
    except Exception as e:
        print(f"[Uploader] Error updating prediction for {image_name}: {e}")



def consume_raw_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='raw_data')
    channel.basic_consume(queue='raw_data', on_message_callback=handle_raw_data, auto_ack=True)
    print("[Uploader] Waiting for raw_data...")
    channel.start_consuming()

def consume_processed_data():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='processed_data')
    channel.basic_consume(queue='processed_data', on_message_callback=handle_processed_data, auto_ack=True)
    print("[Uploader] Waiting for processed_data...")
    channel.start_consuming()

threading.Thread(target=consume_raw_data).start()
threading.Thread(target=consume_processed_data).start()
