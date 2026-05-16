class GeminiProvider:
    """
    Gemini provider adapter.

    Keep provider-specific SDK logic isolated here.
    Do not import Gemini SDK inside agents or business services.
    """

    def generate_structured_response(self, prompt: str, schema: dict | None = None):
        # TODO: integrate Google GenAI SDK here only
        return {
            "success": True,
            "provider": "gemini",
            "data": {}
        }