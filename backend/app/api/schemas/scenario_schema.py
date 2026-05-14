from pydantic import BaseModel


class ScenarioAnalyzeRequest(BaseModel):
    tenant_id: str