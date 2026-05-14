from pydantic import BaseModel


class ReportGenerateRequest(BaseModel):
    tenant_id: str