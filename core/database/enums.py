from enum import Enum


class TypeNotificationEnum(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    
class StatusNotificationEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"