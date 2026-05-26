import json
import os
import re
from typing import Any, Dict, Optional

from google import genai
from google.genai import types

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class GeminiProvider:
    """
    Gemini SDK adapter.

    Only this class talks to google.genai. Agents and services depend on
    the provider interface, never on the SDK directly.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        self._api_key = api_key or os.getenv("GEMINI_API_KEY")
        self._default_model = default_model or os.getenv(
            "GEMINI_MODEL", DEFAULT_GEMINI_MODEL
        )
        self._client: Optional[genai.Client] = None

    def _get_client(self) -> Optional[genai.Client]:
        if not self._api_key:
            return None
        if self._client is None:
            self._client = genai.Client(api_key=self._api_key)
        return self._client

    def generate_json(
        self,
        system_instruction: str,
        user_prompt: str,
        expected_schema: str,
        temperature: float = 0.2,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        client = self._get_client()
        if client is None:
            return _fallback_error("missing_gemini_api_key")

        final_prompt = _build_json_prompt(user_prompt, expected_schema)

        try:
            response = client.models.generate_content(
                model=model or self._default_model,
                contents=final_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    response_mime_type="application/json",
                ),
            )
        except Exception as exc:
            return _fallback_error("llm_service_exception", details=str(exc))

        raw_text = getattr(response, "text", None)
        if not raw_text:
            return _fallback_error("empty_llm_response")

        parsed = _parse_json_safely(raw_text)
        if parsed is None:
            return _fallback_error("invalid_json_response", raw_response=raw_text)
        if not isinstance(parsed, dict):
            return _fallback_error("json_response_not_object", raw_response=raw_text)
        return parsed


def _build_json_prompt(user_prompt: str, expected_schema: str) -> str:
    return f"""You must return ONLY valid JSON.

Do not include:
- markdown
- explanations
- comments
- code fences
- extra text before or after JSON

Expected JSON schema/shape:
{expected_schema}

User request:
{user_prompt}
""".strip()


def _parse_json_safely(raw_text: str) -> Optional[Any]:
    cleaned = raw_text.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    cleaned = _remove_markdown_code_fences(cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    extracted = _extract_first_json_object(cleaned)
    if not extracted:
        return None
    try:
        return json.loads(extracted)
    except json.JSONDecodeError:
        return None


def _remove_markdown_code_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"```$", "", text).strip()
    return text


def _extract_first_json_object(text: str) -> Optional[str]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]


def _fallback_error(
    error: str,
    details: Optional[str] = None,
    raw_response: Optional[str] = None,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {"success": False, "error": error}
    if details:
        result["details"] = details
    if raw_response:
        result["raw_response"] = raw_response
    return result
