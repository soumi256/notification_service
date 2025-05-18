import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect("notifications.db", check_same_thread=False)
cursor = conn.cursor()

# Create notifications table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        message TEXT,
        status TEXT,
        created_at TEXT
    )
''')
conn.commit()

# Store a new notification
def store_notification(user_id, notif_type, message, status):
    cursor.execute(
        "INSERT INTO notifications (user_id, type, message, status, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, notif_type, message, status, datetime.utcnow().isoformat())
    )
    conn.commit()

# Get all notifications for a specific user
def get_user_notifications(user_id):
    cursor.execute("SELECT * FROM notifications WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    notifications = []
    for row in rows:
        notifications.append({
            "id": row[0],
            "user_id": row[1],
            "type": row[2],
            "message": row[3],
            "status": row[4],
            "created_at": row[5]
        })
    return notifications

# Get all notifications in the database
def get_all_notifications():
    cursor.execute("SELECT * FROM notifications")
    rows = cursor.fetchall()
    notifications = []
    for row in rows:
        notifications.append({
            "id": row[0],
            "user_id": row[1],
            "type": row[2],
            "message": row[3],
            "status": row[4],
            "created_at": row[5]
        })
    return notifications

# Update the status of a specific notification
def update_notification_status(user_id, message, new_status):
    cursor.execute(
        "UPDATE notifications SET status = ?, created_at = ? WHERE user_id = ? AND message = ?",
        (new_status, datetime.utcnow().isoformat(), user_id, message)
    )
    conn.commit()
