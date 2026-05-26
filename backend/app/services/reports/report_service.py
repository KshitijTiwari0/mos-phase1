from app.schemas.report_schema import ReportGenerateRequest


class ReportService:
    """
    Manager-summary report builder (Phase 1 stub).

    Real implementation will aggregate conversation logs + agent outputs
    once persistence layer is in place. For now this returns a deterministic
    placeholder so the API contract is callable.
    """

    @staticmethod
    def generate_report(payload: ReportGenerateRequest) -> dict:
        return {
            "tenant_id": payload.tenant_id,
            "status": "not_implemented",
            "summary": (
                "Report generation will be wired up after conversation "
                "logging persistence is added."
            ),
        }
