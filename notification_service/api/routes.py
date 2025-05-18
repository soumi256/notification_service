from fastapi import APIRouter
from pydantic import BaseModel
from message_queue.producer import publish_notification
from db.database import store_notification, get_user_notifications

router = APIRouter()

class NotificationRequest(BaseModel):
    user_id: int
    type: str
    message: str

@router.post("/notifications")
def send_notification(req: NotificationRequest):     
        publish_notification(req.dict())
        store_notification(req.user_id, req.type, req.message, "pending")
        return {"status": "queued"}

@router.get("/users/{user_id}/notifications")
def get_notifications(user_id: int):
     return get_user_notifications(user_id)
