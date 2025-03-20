from pydantic import BaseModel
from typing import List,Tuple


class Source(BaseModel):
    document_id: str
    filename: str
    snippet: str

class ChatbotRequest(BaseModel):
    message: str 
    chat_history: List[Tuple[str, str]]


class ChatbotResponse(BaseModel):
    message: str
    sources: List[Source]