from fastapi import APIRouter

from app.schemas.report_schema import ReportGenerateRequest
from app.services.reports.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate")
def generate_report(payload: ReportGenerateRequest):
    return ReportService.generate_report(payload)