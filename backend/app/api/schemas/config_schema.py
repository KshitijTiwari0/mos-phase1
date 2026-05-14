from pydantic import BaseModel
from typing import Any


class BusinessConfigCreate(BaseModel):
    tenant_id: str
    business_name: str
    industry: str
    tone: str
    primary_goal: str
    products: list[Any] = []
    faqs: list[Any] = []
    qualification_questions: list[Any] = []
    objection_handling: list[Any] = []
    primary_cta: str


class BusinessConfigResponse(BaseModel):
    tenant_id: str
    business_name: str
    industry: str