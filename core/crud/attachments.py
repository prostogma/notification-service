from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Attachment


async def create_attachment(
    session: AsyncSession,
    file_paths: list[str],
    notification_id: UUID
    ):
    for file_path in file_paths:
        attachment = Attachment(
            file_path=file_path,
            notification_id=notification_id
        )
        session.add(attachment)
    
    