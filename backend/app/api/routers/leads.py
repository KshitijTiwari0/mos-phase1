from fastapi import APIRouter

from app.schemas.lead_schema import LeadCreate
from app.services.leads.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/create")
def create_lead(payload: LeadCreate):
    return LeadService.create_lead(payload)