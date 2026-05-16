from pydantic import BaseModel


class LeadCreate(BaseModel):
    tenant_id: str
    name: str
    source: str
    message: str