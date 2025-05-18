import pika
import json
from services.notification_service import send_notification

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(" [x] Received Notification:", data)
    send_notification(data)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')

    channel.basic_consume(
        queue='notifications',
        on_message_callback=callback,
        auto_ack=True
    )

    print(' [*] Waiting for notifications. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
