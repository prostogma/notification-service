from pydantic import BaseModel, EmailStr, Field

from core.database.enums import TypeNotificationEnum

class CreateNotificationScheme(BaseModel):
    type: TypeNotificationEnum
    recipient: EmailStr | str
    subject: str = Field(min_length=3, max_length=100)
    message_text: str | None = None
    message_html: str | None = None
    attachments: list[str]
    
    