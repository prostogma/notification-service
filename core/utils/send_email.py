from uuid import UUID
import aiosmtplib
from email.message import EmailMessage

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db_helper import async_session_maker
from core.database.enums import StatusNotificationEnum
from core.database.models import Notification

async def send_email(notification: Notification):
    email = "no_reply@example.com"
    
    message = EmailMessage()
    message["From"] = email
    message["To"] = notification.recipient
    message["Subject"] = notification.subject
    
    # добавляем текстовую версию
    message.set_content(notification.message_text)
    
    if notification.message_html:
        # добавляем HTML версию
        message.add_alternative(notification.message_html, subtype="html")
    
    await aiosmtplib.send(
        message,
        sender=email,
        recipients=[notification.recipient],
        hostname="maildev",
        port=1025
    )

async def update_notification_status(
    notification_id: UUID,
    status: StatusNotificationEnum
    ):
    async with async_session_maker() as session:
        try:
            stmt = (
                update(Notification)
                .filter(Notification.id == notification_id)
                .values(status=status)
            )
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при работе с сессией - {e}")
            raise
