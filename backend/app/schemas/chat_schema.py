from typing import List, Optional

from pydantic import BaseModel

from app.schemas.agent_schema import BusinessConfig, ConversationTurn, LeadContext


class ChatMessageRequest(BaseModel):
    tenant_id: str
    conversation_id: str
    message: str
    lead_context: Optional[LeadContext] = None
    conversation_history: List[ConversationTurn] = []
    business_config_override: Optional[BusinessConfig] = None
