import json
from typing import Any

from app.schemas.agent_schema import AgentEnvelope


def serialize_history(history: list) -> str:
    if not history:
        return "(no prior conversation)"
    return json.dumps(history, ensure_ascii=False, indent=2)


def serialize_dict(data: Any) -> str:
    if not data:
        return "{}"
    return json.dumps(data, ensure_ascii=False, indent=2)


def envelope_from_llm(agent_name: str, llm_response: Any) -> AgentEnvelope:
    """
    Normalize the raw dict returned by llm_service into an AgentEnvelope.
    llm_service returns {"success": False, "error": ...} on failure,
    otherwise the parsed model output dict.
    """
    if isinstance(llm_response, dict) and llm_response.get("success") is False:
        return AgentEnvelope(
            agent=agent_name,
            success=False,
            error=llm_response.get("error", "unknown_error"),
            error_details=llm_response.get("details"),
            raw_response=llm_response.get("raw_response"),
        )
    if not isinstance(llm_response, dict):
        return AgentEnvelope(
            agent=agent_name,
            success=False,
            error="llm_response_not_dict",
            raw_response=str(llm_response),
        )
    return AgentEnvelope(agent=agent_name, success=True, data=llm_response)
