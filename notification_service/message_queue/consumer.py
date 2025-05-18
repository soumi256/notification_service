import pika
import json
from db.database import store_notification  # adjust import if needed

def send_notification_simulation(notification):
    print(f"Simulating sending {notification['type']} notification to user {notification['user_id']}: {notification['message']}")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        print(f" [x] Received notification from queue: {data}")

        required_keys = {"user_id", "type", "message", "status"}
        if not required_keys.issubset(data.keys()):
            print(" [!] Incomplete notification data, skipping...")
            ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge message even if incomplete
            return

        # Try to store notification in DB
        try:
            store_notification(
                user_id=data["user_id"],
                type=data["type"],
                message=data["message"],
                status=data["status"]
            )
            print(" [✓] Stored notification in database.")
        except Exception as e:
            print(f" [!] Failed to store notification: {e}")
            # Reject message and requeue for retry
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return

        # Simulate sending Email/SMS notification
        send_notification_simulation(data)

        # Acknowledge message after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError:
        print(" [!] Failed to decode JSON from message.")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Ack to discard bad message
    except Exception as e:
        print(f" [!] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Requeue on unknown errors

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    # Turn off auto_ack for manual ack/nack
    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=False)
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume()
