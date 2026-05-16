# backend/app/services/llm/llm_service.py

import json
import os
import re
from typing import Any, Dict, Optional

from google import genai
from google.genai import types


DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


def generate_json_response(
    system_instruction: str,
    user_prompt: str,
    expected_schema: str,
    temperature: float = 0.2,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Centralized LLM service for MOS Phase 1.

    Rules:
    - Only this service talks to Gemini.
    - Agents must call this function instead of importing Gemini directly.
    - Always returns a JSON-compatible dict.
    """

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return _fallback_error("missing_gemini_api_key")

        client = genai.Client(api_key=api_key)

        final_prompt = _build_json_prompt(
            user_prompt=user_prompt,
            expected_schema=expected_schema,
        )

        response = client.models.generate_content(
            model=model or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL),
            contents=final_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )

        raw_text = getattr(response, "text", None)

        if not raw_text:
            return _fallback_error("empty_llm_response")

        parsed = _parse_json_safely(raw_text)

        if parsed is None:
            return _fallback_error(
                "invalid_json_response",
                raw_response=raw_text,
            )

        if not isinstance(parsed, dict):
            return _fallback_error(
                "json_response_not_object",
                raw_response=raw_text,
            )

        return parsed

    except Exception as exc:
        return _fallback_error(
            "llm_service_exception",
            details=str(exc),
        )


def _build_json_prompt(
    user_prompt: str,
    expected_schema: str,
) -> str:
    return f"""
You must return ONLY valid JSON.

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
    """
    Attempts strict JSON parsing first.
    Falls back to extracting the first JSON object from noisy output.
    """

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
    result: Dict[str, Any] = {
        "success": False,
        "error": error,
    }

    if details:
        result["details"] = details

    if raw_response:
        result["raw_response"] = raw_response

    return result