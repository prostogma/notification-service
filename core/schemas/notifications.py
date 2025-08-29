from uuid import UUID
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from core.database.enums import StatusNotificationEnum, TypeNotificationEnum

class CreateNotificationScheme(BaseModel):
    type: TypeNotificationEnum
    recipient: str
    subject: str = Field(min_length=3, max_length=100)
    message_text: str | None = None
    message_html: str | None = None
    attachments: list[str] | None = None
    
    @model_validator(mode="after")
    def check_recipient(self):
        if self.type == TypeNotificationEnum.EMAIL:
            try:
                validate_email(self.recipient)
            except EmailNotValidError:
                raise ValueError("recipient должен быть корректным email при type=email")
        elif self.type == TypeNotificationEnum.SMS:
            try:
                parsed = phonenumbers.parse(self.recipient, "RU")
                phonenumbers.is_valid_number(parsed)
            except NumberParseException:
                raise ValueError("recipient должен быть корректным номером телефона при type=sms")
        return self

class NotificationScheme(BaseModel):
    id: UUID
    type: TypeNotificationEnum
    recipient: str
    subject: str
    status: StatusNotificationEnum
    message_text: str | None = None
    message_html: str | None = None
    
    model_config = ConfigDict(
        from_attributes=True,
    )
    
class NotificationFilterScheme(BaseModel):
    limit: int = Field(default=100, gt=0, lt=3000)
    offset: int = Field(default=0, ge=0)
    type: TypeNotificationEnum | None = None
    status: StatusNotificationEnum | None = None
    