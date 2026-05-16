from app.services.llm.llm_service import LLMService


class AnalyticsAgent:
    @staticmethod
    def run(agent_input: dict):
        return LLMService.generate_structured_response(
            prompt="TODO: analytics prompt",
            schema={}
        )