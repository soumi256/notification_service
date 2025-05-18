# Notification Service

## Overview

This project implements a Notification Service with the following features:
- Accepts notifications via RabbitMQ message queue
- Stores notifications in a SQLite database
- Supports retry logic to handle failures during storing
- Simulates sending notifications via Email, SMS, and In-App channels
- Provides REST API endpoints to fetch and update notifications

---

## System Architecture

+-------------+ +----------------+ +-----------------+
| Notification| --> | RabbitMQ Queue | --> | Notification |
| Producer | | "notifications"| | Consumer |
+-------------+ +----------------+ +-----------------+
|
v
+---------------------+
| SQLite Database |
| (Notifications) |
+---------------------+
|
v
+---------------------+
| Simulated Senders: |
| Email / SMS / In-App |
+---------------------+

REST API Server
|
+---> Exposes endpoints to retrieve and update notifications



---

## Tech Stack

| Component       | Technology/Library          |
|-----------------|----------------------------|
| Message Queue   | RabbitMQ (pika Python lib) |
| Database        | SQLite (sqlite3)           |
| Backend         | Python, FastAPI            |
| Message Consumer| Python (pika)              |
| Logging         | Python logging module      |

---

## How to Run

### Prerequisites

- Python 3.8+
- RabbitMQ server running locally (default on localhost:5672)
- SQLite (no setup required, embedded file DB)

### Steps

1. **Start RabbitMQ**  
Make sure RabbitMQ is running on your machine.

2. **Run the consumer service**  
```bash
python consumer.py
This will connect to RabbitMQ, consume notifications, store them in SQLite, and simulate sending.

Run the REST API server

bash
Copy code
uvicorn main:app --reload
Replace main.py with your FastAPI app file.

API will be available at http://localhost:8000

REST API Endpoints
Get notifications for a user
http
Copy code
GET /notifications/{user_id}
Response example:

json

[
  {
    "id": 1,
    "user_id": "123",
    "type": "email",
    "message": "Your order has been shipped",
    "status": "sent"
  },
  ...
]
Update notification status
http
Copy code
PUT /notifications/{notification_id}
Content-Type: application/json

{
  "status": "read"
}
Response:

json
Copy code
{
  "id": 1,
  "user_id": "123",
  "type": "email",
  "message": "Your order has been shipped",
  "status": "read"
}
Example Notification Message (for RabbitMQ)
json

{
  "user_id": "123",
  "type": "email",
  "message": "Welcome to our service!",
  "status": "pending"
}
Retry Logic
If storing a notification fails (e.g., DB down), the consumer will reject the message without acknowledgement, causing RabbitMQ to requeue and retry later.

This ensures no messages are lost.

Logging
Logs are saved to consumer.log for debugging and audit purposes.

Example log entry:

pgsql

INFO - Processed notification: {'user_id': '123', 'type': 'email', 'message': 'Hello!', 'status': 'pending'}
Optional Enhancements (Future Work)
Integrate real Email/SMS sending via services like SendGrid or Twilio

Dockerize the whole application for easier deployment

Create a frontend dashboard to view and manage notifications

Contact
For questions or contributions, please contact: soumi042016@gmail.com



---

If you want, I can help you generate this as a file or customize it further for your repo. Just let me know!






