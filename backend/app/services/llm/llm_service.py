from app.services.llm.providers.gemini_provider import GeminiProvider


class LLMService:
    """
    Central LLM boundary.
    All agents/services must call this service only.
    No direct Gemini calls outside this module/provider layer.
    """

    provider = GeminiProvider()

    @classmethod
    def generate_structured_response(cls, prompt: str, schema: dict | None = None):
        return cls.provider.generate_structured_response(
            prompt=prompt,
            schema=schema
        )