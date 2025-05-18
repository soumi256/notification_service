from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from notification_service.db.database import store_notification, get_user_notifications, get_all_notifications, update_notification_status
from notification_service.message_queue import producer

app = FastAPI()

# Pydantic models
class Notification(BaseModel):
    user_id: int
    type: str
    message: str
    status: str

class UpdateStatus(BaseModel):
    user_id: int
    message: str
    new_status: str

@app.post("/notifications/")
def create_notification(notification: Notification):
    try:
        # Push to queue only — database insert happens in the consumer
        producer.publish_notification(notification.dict())
        return {"message": "Notification pushed to queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/notifications/user/{user_id}")
def fetch_user_notifications(user_id: int):
    try:
        return get_user_notifications(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notifications/")
def fetch_all_notifications():
    try:
        return get_all_notifications()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notifications/update-status")
def update_status(data: UpdateStatus):
    try:
        update_notification_status(data.user_id, data.message, data.new_status)
        return {"message": "Notification status updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
