import pika
import json

def publish_notification(notification_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')

    channel.basic_publish(
        exchange='',
        routing_key='notifications',
        body=json.dumps(notification_data)

    )
    print(" [x] Sent notification to queue")
    connection.close()

if __name__ == "__main__":
    print("[*] Running producer script...")  # DEBUG
    notification_data = {
        "user_id": 1,
        "type": "email",
        "message": "Welcome to our service!",
        "status": "pending"
    }

    publish_notification(notification_data)


    