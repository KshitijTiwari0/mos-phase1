from app.services.llm.llm_service import LLMService


class SalesAgent:
    @staticmethod
    def run(agent_input: dict):
        # TODO: build prompt from config + lead context + conversation history
        return LLMService.generate_structured_response(
            prompt="TODO: sales prompt",
            schema={}
        )