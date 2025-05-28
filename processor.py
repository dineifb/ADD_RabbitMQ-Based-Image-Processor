import pika
import json
import random
import time

# Simulated model prediction
def simulate_prediction():
    label = random.choice(["cat", "dog"])
    confidence = round(random.uniform(0.7, 0.99), 2)
    return label, confidence

# RabbitMQ callback
def callback(ch, method, properties, body):
    data = json.loads(body)
    image_name = data.get('image_name')
    file_path = data.get('file_path')

    print(f"[Processor] Received image: {image_name}")

    # Simulate image loading & prediction
    time.sleep(1)  # simulate processing delay
    prediction, confidence = simulate_prediction()

    result = {
        "image_name": image_name,
        "prediction": prediction,
        "confidence": confidence
    }

    # Send prediction to another queue
    channel.basic_publish(
        exchange='',
        routing_key='processed_data',
        body=json.dumps(result)
    )
    print(f"[Processor] Sent prediction: {result}")

# Setup RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='raw_data')
channel.queue_declare(queue='processed_data')

channel.basic_consume(queue='raw_data', on_message_callback=callback, auto_ack=True)

print("[Processor] Waiting for image metadata...")
channel.start_consuming()





