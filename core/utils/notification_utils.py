from fastapi import HTTPException, status
from core.database.enums import TypeNotificationEnum
from core.schemas.notifications import CreateNotificationScheme


async def validate_notification_data(notification_data: CreateNotificationScheme):
    if not notification_data.message_html_b64 and notification_data.attachments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя передать вложения, при пустом html сообщении!"
        )
        
    if notification_data.type == TypeNotificationEnum.SMS:
        if notification_data.message_html_b64:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя передать html, в sms сообщение!"
        )
        elif notification_data.attachments:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя передать вложения, в sms сообщение!"
        )
        elif not notification_data.message_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="SMS должно содержать текст сообщения!"
            )
            