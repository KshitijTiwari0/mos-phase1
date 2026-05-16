from app.schemas.lead_schema import LeadCreate


class LeadService:
    @staticmethod
    def create_lead(payload: LeadCreate):
        # TODO:
        # 1. Store lead
        # 2. Trigger orchestrator/analytics flow later

        return {
            "lead_id": "lead_001",
            "status": "received"
        }