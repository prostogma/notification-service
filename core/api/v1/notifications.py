from typing import Annotated
from fastapi import APIRouter, Body

from core.crud.notifications import create_notification
from core.database.db_helper import session_DB
from core.schemas.notifications import CreateNotificationScheme, NotificationScheme


router = APIRouter(prefix="/notifications", tags=["Уведомления 📢"])

@router.post("/", response_model=NotificationScheme)
async def create_notification_handler(
    session: session_DB,
    notification_data: Annotated[CreateNotificationScheme, Body()]
    ):
    notification = await create_notification(session, notification_data)
    return notification