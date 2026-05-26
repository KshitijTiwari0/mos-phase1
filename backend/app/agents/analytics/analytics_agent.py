from typing import Union

from app.agents.base import envelope_from_llm, serialize_dict, serialize_history
from app.prompts.loader import load_prompt, wrap_untrusted
from app.schemas.agent_schema import AgentEnvelope, AgentInput, AnalyticsAgentData
from app.services.llm.llm_service import generate_json_response

AGENT_NAME = "analytics_ai"

EXPECTED_SCHEMA = """
{
  "agent": "analytics_ai",
  "score": 0,
  "intent": "string",
  "category": "hot_lead | warm_lead | cold_lead | spam",
  "recommended_action": "sales_followup | qualification | nurture | support_routing | ignore"
}
""".strip()


def run(agent_input: AgentInput) -> AgentEnvelope:
    bc = agent_input.business_config

    system_instruction = load_prompt(
        "analytics_system.txt",
        business_name=bc.business_name,
        industry=bc.industry,
        primary_goal=bc.primary_goal,
        primary_cta=bc.primary_cta,
        qualification_questions=serialize_dict(bc.qualification_questions),
    )

    user_prompt = load_prompt(
        "analytics_user.txt",
        lead_context=wrap_untrusted(
            "lead_context", serialize_dict(agent_input.lead_context.model_dump())
        ),
        conversation_history=wrap_untrusted(
            "conversation_history",
            serialize_history(
                [t.model_dump() for t in agent_input.conversation_history]
            ),
        ),
        customer_message=wrap_untrusted(
            "customer_message", agent_input.customer_message
        ),
    )

    raw = generate_json_response(
        system_instruction=system_instruction,
        user_prompt=user_prompt,
        expected_schema=EXPECTED_SCHEMA,
        temperature=0.2,
    )

    envelope = envelope_from_llm(AGENT_NAME, raw)
    if not envelope.success:
        return envelope

    try:
        validated = AnalyticsAgentData(**(envelope.data or {}))
    except Exception as exc:
        return AgentEnvelope(
            agent=AGENT_NAME,
            success=False,
            error="output_schema_validation_failed",
            error_details=str(exc),
            raw_response=str(envelope.data),
        )

    envelope.data = validated.model_dump()
    return envelope


class AnalyticsAgent:
    """Backwards-compatible facade. Accepts dict or AgentInput, returns dict."""

    @staticmethod
    def run(agent_input: Union[AgentInput, dict]) -> dict:
        if isinstance(agent_input, dict):
            agent_input = AgentInput(**agent_input)
        return run(agent_input).model_dump()
