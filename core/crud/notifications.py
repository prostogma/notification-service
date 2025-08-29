from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.crud.attachments import create_attachment
from core.database.models import Notification
from core.schemas.notifications import CreateNotificationScheme, NotificationFilterScheme
from core.utils.validate_notification import validate_notification_data


async def create_notification(
    session: AsyncSession,
    notification_data: CreateNotificationScheme
):
    await validate_notification_data(notification_data)
        
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

async def get_notifications(
    session: AsyncSession,
    filter_query: NotificationFilterScheme
):
    stmt = select(Notification).limit(filter_query.limit).offset(filter_query.offset)
    
    if filter_query.type:
        stmt = stmt.filter(Notification.type == filter_query.type)
    elif filter_query.status:
        stmt = stmt.filter(Notification.status == filter_query.status)
    
    result = await session.execute(stmt)
    notifications = result.scalars().all()
    
    return notifications

async def get_notification(
    session: AsyncSession,
    notification_id: UUID
):
    stmt = select(Notification).filter(Notification.id == notification_id)
    result = await session.execute(stmt)
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление с таким id не найдено!"
        )
    
    return notification
    
    
    