from typing import Any, Dict

from app.agents.analytics import analytics_agent
from app.agents.sales import sales_agent
from app.schemas.agent_schema import (
    AgentInput,
    AnalyticsAgentData,
    BusinessConfig,
    LeadContext,
)
from app.schemas.chat_schema import ChatMessageRequest
from app.services.config.config_service import ConfigService

_SALES_TRIGGER_ACTIONS = {"sales_followup", "qualification", "nurture"}


class OrchestratorService:
    """
    Backend controller/router.
    Wires the Phase 1 multi-agent pipeline:
        business_config -> AnalyticsAgent -> (optional) SalesAgent -> response
    """

    @staticmethod
    def process_chat_message(payload: ChatMessageRequest) -> Dict[str, Any]:
        business_config = OrchestratorService._resolve_business_config(payload)
        lead_context = payload.lead_context or LeadContext()
        history = list(payload.conversation_history or [])

        analytics_input = AgentInput(
            tenant_id=payload.tenant_id,
            customer_message=payload.message,
            business_config=business_config,
            lead_context=lead_context,
            conversation_history=history,
        )
        analytics_envelope = analytics_agent.run(analytics_input)

        result: Dict[str, Any] = {
            "tenant_id": payload.tenant_id,
            "conversation_id": payload.conversation_id,
            "analytics": analytics_envelope.model_dump(),
            "sales": None,
            "route": "analytics_failed",
        }

        if not analytics_envelope.success:
            return result

        analytics_data = AnalyticsAgentData(**analytics_envelope.data)

        if analytics_data.recommended_action not in _SALES_TRIGGER_ACTIONS:
            result["route"] = f"skipped_sales:{analytics_data.recommended_action}"
            return result

        sales_input = AgentInput(
            tenant_id=payload.tenant_id,
            customer_message=payload.message,
            business_config=business_config,
            lead_context=lead_context,
            conversation_history=history,
            analytics_signal=analytics_data,
        )
        sales_envelope = sales_agent.run(sales_input)
        result["sales"] = sales_envelope.model_dump()
        result["route"] = "analytics_to_sales"
        return result

    @staticmethod
    def _resolve_business_config(payload: ChatMessageRequest) -> BusinessConfig:
        if payload.business_config_override is not None:
            return payload.business_config_override
        raw = ConfigService.get_config(payload.tenant_id) or {}
        return BusinessConfig(**raw)
