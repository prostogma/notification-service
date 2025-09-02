from pydantic import BaseModel


class AttachmentScheme(BaseModel):
    file_path: str