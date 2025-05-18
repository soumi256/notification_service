def send_notification(data):
    # Implement your logic to send notification
    # For now, just print what would be sent
    print(f"Sending notification to User ID: {data['user_id']}")
    print(f"Notification Type: {data['type']}")
    print(f"Message: {data.get('message', 'No message')}")
