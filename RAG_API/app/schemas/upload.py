from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    document_id: str


