from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from models.auth import User
from models.notification import Notification
from models.schemas import NotificationSchema, NotificationCreate
from core.security import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

def check_role(required_roles: list):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.value not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker

@router.get("/", response_model=list[NotificationSchema])
def get_notifications(
    is_read: bool | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Notification).filter(Notification.recipient_id == current_user.id)
    
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    notifications = query.offset(skip).limit(limit).all()
    return notifications

@router.post("/", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED)
def send_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin", "instructor"]))
):
    db_notification = Notification(**notification.dict(), sender_id=current_user.id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.put("/{notification_id}/read", response_model=NotificationSchema)
def mark_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    if str(notification.recipient_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    notification.is_read = True
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

@router.put("/read-all")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db.query(Notification).filter(
        Notification.recipient_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    if str(notification.recipient_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    
    db.delete(notification)
    db.commit()

@router.post("/broadcast", status_code=status.HTTP_201_CREATED)
def broadcast_notification(
    title: str = Query(...),
    message: str = Query(...),
    notification_type: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(check_role(["admin"]))
):
    users = db.query(User).filter(User.is_active == True).all()
    
    notifications = [
        Notification(
            recipient_id=user.id,
            sender_id=current_user.id,
            title=title,
            message=message,
            notification_type=notification_type,
            channel="in_app"
        ) for user in users
    ]
    
    db.add_all(notifications)
    db.commit()
    return {"message": f"Broadcast sent to {len(notifications)} users"}
