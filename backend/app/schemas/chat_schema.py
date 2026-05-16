from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    tenant_id: str
    conversation_id: str
    message: str