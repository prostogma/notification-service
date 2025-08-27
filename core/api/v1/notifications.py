from typing import Annotated
from fastapi import APIRouter, Form

from core.database.db_helper import session_DB
from core.schemas.notifications import CreateNotificationScheme


router = APIRouter(prefix="/notifications", tags=["Уведомления 📢"])

@router.post("/")
async def create_notification_handler(
    session: session_DB,
    notification: Annotated[CreateNotificationScheme, Form()]
    ):
    ...