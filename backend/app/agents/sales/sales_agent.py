from typing import List, Union

from app.agents.base import envelope_from_llm, serialize_dict, serialize_history
from app.prompts.loader import load_prompt, wrap_untrusted
from app.schemas.agent_schema import AgentEnvelope, AgentInput, SalesAgentData
from app.services.llm.llm_service import generate_json_response

AGENT_NAME = "sales_ai"

EXPECTED_SCHEMA = """
{
  "agent": "sales_ai",
  "response_text": "string in the configured business tone",
  "next_action": "string",
  "intent": "string",
  "confidence": 0.0
}
""".strip()


def _find_do_not_say_violations(
    response_text: str, do_not_say: List[str]
) -> List[str]:
    lowered = response_text.lower()
    return [phrase for phrase in do_not_say if phrase and phrase.lower() in lowered]


def run(agent_input: AgentInput) -> AgentEnvelope:
    bc = agent_input.business_config

    system_instruction = load_prompt(
        "sales_system.txt",
        business_name=bc.business_name,
        industry=bc.industry,
        tone=bc.tone,
        primary_goal=bc.primary_goal,
        primary_cta=bc.primary_cta,
        products=serialize_dict(bc.products),
        faqs=serialize_dict(bc.faqs),
        qualification_questions=serialize_dict(bc.qualification_questions),
        objection_handling=serialize_dict(bc.objection_handling),
        do_not_say=serialize_dict(bc.do_not_say),
    )

    if agent_input.analytics_signal is not None:
        analytics_block = wrap_untrusted(
            "analytics_signal",
            serialize_dict(agent_input.analytics_signal.model_dump()),
        )
    else:
        analytics_block = "(no analytics signal available — treat as cold lead)"

    user_prompt = load_prompt(
        "sales_user.txt",
        analytics_signal=analytics_block,
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
        temperature=0.3,
    )

    envelope = envelope_from_llm(AGENT_NAME, raw)
    if not envelope.success:
        return envelope

    try:
        validated = SalesAgentData(**(envelope.data or {}))
    except Exception as exc:
        return AgentEnvelope(
            agent=AGENT_NAME,
            success=False,
            error="output_schema_validation_failed",
            error_details=str(exc),
            raw_response=str(envelope.data),
        )

    data = validated.model_dump()
    violations = _find_do_not_say_violations(validated.response_text, bc.do_not_say)
    if violations:
        data["policy_violations"] = violations
        data["response_text"] = (
            "[REDACTED — generated text contained restricted phrases; "
            "regenerate with stronger guidance.]"
        )

    envelope.data = data
    return envelope


class SalesAgent:
    """Backwards-compatible facade. Accepts dict or AgentInput, returns dict."""

    @staticmethod
    def run(agent_input: Union[AgentInput, dict]) -> dict:
        if isinstance(agent_input, dict):
            agent_input = AgentInput(**agent_input)
        return run(agent_input).model_dump()
