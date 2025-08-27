from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

from core.database.enums import StatusNotificationEnum, TypeNotificationEnum


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

class Notification(Base):
    __tablename__="notifications"
    
    type: Mapped[TypeNotificationEnum]
    recipient: Mapped[str]
    subject: Mapped[str] = mapped_column(String(100))
    message_text: Mapped[str] = mapped_column(nullable=True)
    message_html: Mapped[str | None] = mapped_column(nullable=True)
    status: Mapped[StatusNotificationEnum] = mapped_column(default=StatusNotificationEnum.PENDING)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        back_populates="notification",
        lazy="selectin"
    )
    
class Attachment(Base):
    __tablename__="attachments"
    
    file_path: Mapped[str]
    notification_id: Mapped[UUID] = mapped_column(ForeignKey("notifications.id", ondelete="CASCADE"))
    
    notification: Mapped["Notification"] = relationship(
        "Notification",
        back_populates="attachments",
        lazy="selectin"
        )
    
    