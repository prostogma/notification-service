from sqlalchemy.ext.asyncio import AsyncSession

from core.crud.attachments import create_attachment
from core.database.enums import TypeNotificationEnum
from core.database.models import Notification
from core.schemas.notifications import CreateNotificationScheme


async def create_notification(
    session: AsyncSession,
    notification_data: CreateNotificationScheme
    ):
    notification_data_dict = notification_data.model_dump(exclude_unset=True)
    notification_data_dict.pop("attachments", None)
    notification = Notification(**notification_data_dict)
    
    session.add(notification)
    await session.flush()    
    
    if notification_data.attachments:
        await create_attachment(session, notification_data.attachments, notification.id)
    
    await session.commit()
    await session.refresh(notification)
    return notification
    
    