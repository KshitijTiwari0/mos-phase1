# backend/app/schemas/chat_schema.py
from typing import Optional
from pydantic import BaseModel


class ChatMessageRequest(BaseModel):
    tenant_id: str
    customer_id: str
    message: str
    conversation_id: Optional[str] = None


class AnalyticsSummarySchema(BaseModel):
    score: int
    category: str
    recommended_action: str


class ChatMessageResponse(BaseModel):
    conversation_id: str
    response_text: str
    agent: str
    intent: str
    analytics: AnalyticsSummarySchema