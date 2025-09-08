from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Body, Query

from core.crud.notifications import create_notification, get_notification, get_notifications
from core.database.db_helper import session_DB
from core.database.enums import TypeNotificationEnum
from core.schemas.notifications import CreateNotificationScheme, NotificationFilterScheme, NotificationScheme
from core.tasks.email_tasks import send_email_task


router = APIRouter(prefix="/notifications", tags=["Уведомления 📢"])

@router.post("/", response_model=NotificationScheme)
async def create_notification_handler(
    session: session_DB,
    notification_data: Annotated[CreateNotificationScheme, Body()]
):
    notification = await create_notification(session, notification_data)
    if notification_data.type == TypeNotificationEnum.EMAIL:
        send_email_task.delay(notification.id)
    return notification

@router.get("/", response_model=list[NotificationScheme])
async def get_notifications_handler(
    session: session_DB,
    filter_query: Annotated[NotificationFilterScheme, Query()]
):
    notifications = await get_notifications(session, filter_query)
    return notifications

@router.get("/{notification_id}/", response_model=NotificationScheme)
async def get_notification_handler(
    session: session_DB,
    notification_id: UUID
):
    notification = await get_notification(session, notification_id)
    return notification