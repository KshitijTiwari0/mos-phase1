from app.schemas.scenario_schema import ScenarioAnalyzeRequest


class ScenarioService:
    """
    Scenario / pattern analysis service (Phase 1 stub).

    Real implementation will run pattern detection on the conversation
    log history. For now this returns a deterministic placeholder so the
    API contract is callable.
    """

    @staticmethod
    def analyze(payload: ScenarioAnalyzeRequest) -> dict:
        return {
            "tenant_id": payload.tenant_id,
            "status": "not_implemented",
            "patterns": [],
        }
