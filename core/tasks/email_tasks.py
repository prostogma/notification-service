import asyncio
import logging

from datetime import datetime, timezone
from uuid import UUID

from core.celery_app import app
from core.crud.notifications import get_notification
from core.database.enums import StatusNotificationEnum
from core.database.db_helper import async_session_maker
from core.utils.send_email import update_notification_status, send_email


logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


@app.task(bind=True, max_retries=3, default_retry_delay=30)
def send_email_task(self, notification_id: UUID):
    result = loop.run_until_complete(_send_email_task(self, notification_id))
    return result
    
async def _send_email_task(self, notification_id: UUID):
    notification = await get_notification(async_session_maker(), notification_id)
    try:
        await update_notification_status(notification.id, StatusNotificationEnum.PROCESSING)
        await asyncio.sleep(5)
        await send_email(notification)
        await update_notification_status(notification.id, StatusNotificationEnum.SENT)
        
        result = {
            "status": "sent",
            "email": notification.recipient,
            "subject": notification.subject,
            "sent_at": datetime.now(timezone.utc),
            "task_id": self.request.id
        }
        
        logger.info(f"Письмо успешно отправленно на {notification.recipient}")
        return result
    except Exception as exc:
        if self.request.retries >= self.max_retries: 
            await update_notification_status(notification.id, StatusNotificationEnum.FAILED)
            
        logger.exception(f"Ошибка при отправке письма на {notification.recipient}: {str(exc)}")
        raise self.retry(exc=exc)
    


