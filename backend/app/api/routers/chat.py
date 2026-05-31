# backend/app/api/routers/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat_schema import ChatMessageRequest
from app.services.orchestrator.orchestrator_service import OrchestratorService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/message")
def send_chat_message(payload: ChatMessageRequest, db: Session = Depends(get_db)):
    """
    Main communication engine entry point.
    Receives user message context and delegates thread synchronization route to Orchestrator.
    """
    return OrchestratorService.process_chat_message(payload, db)