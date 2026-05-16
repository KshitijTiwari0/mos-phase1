from app.schemas.chat_schema import ChatMessageRequest


class OrchestratorService:
    """
    Backend controller/router.
    Not an AI agent.
    Responsible for routing workflow execution.
    """

    @staticmethod
    def process_chat_message(payload: ChatMessageRequest):
        # TODO:
        # 1. Load business config
        # 2. Load conversation history
        # 3. Decide agent route
        # 4. Call appropriate service/agent
        # 5. Log conversation turn
        # 6. Store structured agent output

        return {
            "response_text": "TODO: sales/support response will be generated here",
            "agent": "sales_ai",
            "intent": "unknown"
        }