from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ConversationTurn(BaseModel):
    role: str
    message: str


class LeadContext(BaseModel):
    model_config = ConfigDict(extra="allow")
    source: Optional[str] = None
    lead_name: Optional[str] = None


class BusinessConfig(BaseModel):
    model_config = ConfigDict(extra="allow")
    business_name: str = "N/A"
    industry: str = "N/A"
    tone: str = "Professional English"
    primary_goal: str = ""
    primary_cta: str = ""
    products: List[Any] = []
    faqs: List[Any] = []
    qualification_questions: List[Any] = []
    objection_handling: List[Any] = []
    do_not_say: List[str] = []


class AnalyticsAgentData(BaseModel):
    agent: str = "analytics_ai"
    score: int = Field(ge=0, le=100)
    intent: str
    category: str
    recommended_action: str


class SalesAgentData(BaseModel):
    agent: str = "sales_ai"
    response_text: str
    next_action: str
    intent: str
    confidence: float = Field(ge=0.0, le=1.0)


class AgentInput(BaseModel):
    tenant_id: str
    customer_message: str
    business_config: BusinessConfig
    lead_context: LeadContext = Field(default_factory=LeadContext)
    conversation_history: List[ConversationTurn] = []
    analytics_signal: Optional[AnalyticsAgentData] = None


class AgentEnvelope(BaseModel):
    agent: str
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    error_details: Optional[str] = None
    raw_response: Optional[str] = None
