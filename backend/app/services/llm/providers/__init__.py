import os
from typing import Any, Dict, Optional, Protocol


class LLMProvider(Protocol):
    def generate_json(
        self,
        system_instruction: str,
        user_prompt: str,
        expected_schema: str,
        temperature: float,
        model: Optional[str],
    ) -> Dict[str, Any]: ...


def get_default_provider() -> LLMProvider:
    name = os.getenv("LLM_PROVIDER", "gemini").lower()
    if name == "gemini":
        from app.services.llm.providers.gemini_provider import GeminiProvider

        return GeminiProvider()
    raise ValueError(f"Unsupported LLM provider: {name}")
