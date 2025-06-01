import pika
import json
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import os

model = load_model("cats_vs_dogs_model.h5")
BASE_DIR = os.getcwd()

def preprocess_and_predict(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"[Processor] File not found: {file_path}")
            return "error", 0.0

        img = keras_image.load_img(file_path, target_size=(128, 128))
        img_array = keras_image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array, verbose=0)[0][0]
        label = "cat" if prediction < 0.5 else "dog"
        confidence = round(float(prediction), 2)

        return label, confidence
    except Exception as e:
        print(f"[Processor] Error processing {file_path}: {e}")
        return "error", 0.0

def callback(ch, method, properties, body):
    data = json.loads(body)
    image_name = data.get('image_name')
    print(f"[Processor] Sending result for image_name: '{image_name}'")
    relative_path = data.get('file_path')
    file_path = os.path.join(BASE_DIR, relative_path)
    print(f"[Processor] Trying to access file: {file_path}")
    print(f"[Processor] File exists? {os.path.exists(file_path)}")
    print(f"[Processor] Received image: {image_name}")

    prediction, confidence = preprocess_and_predict(file_path)

    result = {
        "image_name": image_name,
        "prediction": prediction,
        "confidence": confidence
    }

    channel.basic_publish(
        exchange='',
        routing_key='processed_data',
        body=json.dumps(result)
    )
    print(f"[Processor] Sent prediction: {result}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='raw_data')
channel.queue_declare(queue='processed_data')
channel.basic_consume(queue='raw_data', on_message_callback=callback, auto_ack=True)

print("[Processor] Waiting for image metadata...")
channel.start_consuming()
