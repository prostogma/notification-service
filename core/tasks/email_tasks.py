import asyncio
import logging

from datetime import datetime, timezone

from core.celery_app import app
from core.utils.send_email import send_email


logger = logging.getLogger(__name__)


@app.task(bind=True, max_retries=3, default_retry_delay=30)
def send_email_task(self, email: str, subject: str, message: str):
    try:
        asyncio.run(asyncio.sleep(5))
        asyncio.run(send_email(email, subject, message))
        
        result = {
            "status": "sent",
            "email": email,
            "subject": subject,
            "message": message,
            "sent_at": datetime.now(timezone.utc),
            "task_id": self.request.id
        }
        
        logger.info(f"Письмо успешно отправленно на {email}")
        return result
    except Exception as exc:
        logger.exception(f"Ошибка при отправке письма на {email}: {str(exc)}")
        raise self.retry(exc=exc)

