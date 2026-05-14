from fastapi import APIRouter

from app.schemas.chat_schema import ChatMessageRequest
from app.services.orchestrator.orchestrator_service import OrchestratorService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message")
def process_chat_message(payload: ChatMessageRequest):
    return OrchestratorService.process_chat_message(payload)