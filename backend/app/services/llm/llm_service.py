# backend/app/services/llm/llm_service.py

from typing import Any, Dict, Optional

from dotenv import load_dotenv

from app.services.llm.providers import LLMProvider, get_default_provider

load_dotenv()


def generate_json_response(
    system_instruction: str,
    user_prompt: str,
    expected_schema: str,
    temperature: float = 0.2,
    model: Optional[str] = None,
    provider: Optional[LLMProvider] = None,
) -> Dict[str, Any]:
    """
    Provider-agnostic JSON-mode LLM call for MOS Phase 1.

    Rules:
    - Only providers talk to vendor SDKs.
    - Agents must call this function instead of importing any SDK directly.
    - Always returns a JSON-compatible dict.
    """
    selected = provider or get_default_provider()
    return selected.generate_json(
        system_instruction=system_instruction,
        user_prompt=user_prompt,
        expected_schema=expected_schema,
        temperature=temperature,
        model=model,
    )
