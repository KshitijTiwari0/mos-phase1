from fastapi import APIRouter

from app.schemas.scenario_schema import ScenarioAnalyzeRequest
from app.services.scenario.scenario_service import ScenarioService

router = APIRouter(prefix="/scenario", tags=["Scenario"])


@router.post("/analyze")
def analyze_scenario(payload: ScenarioAnalyzeRequest):
    return ScenarioService.analyze(payload)