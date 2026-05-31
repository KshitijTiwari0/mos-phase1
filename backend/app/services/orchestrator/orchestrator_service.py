# backend/app/services/orchestrator/orchestrator_service.py
import json
from uuid import uuid4
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.chat_schema import ChatMessageRequest
from app.agents.analytics.analytics_agent import AnalyticsAgent
from app.agents.sales.sales_agent import SalesAgent


class OrchestratorService:
    """
    Backend orchestration controller layer.
    Manages state, invokes specialized AI agents sequentially, 
    and handles data lifecycle persistence to SQLite.
    """

    @staticmethod
    def process_chat_message(payload: ChatMessageRequest, db: Session) -> dict:
        tenant_id = payload.tenant_id
        customer_id = payload.customer_id
        conversation_id = payload.conversation_id or f"conv_{uuid4().hex[:8]}"
        customer_message = payload.message

        # 1. Fetch Tenant and Business Configuration from Database
        tenant = db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()
        if not tenant:
            tenant = models.Tenant(id=tenant_id, name=f"Auto Generated Tenant {tenant_id}")
            db.add(tenant)
            db.commit()

        config_record = db.query(models.BusinessConfig).filter(
            models.BusinessConfig.tenant_id == tenant_id
        ).order_by(models.BusinessConfig.id.desc()).first()

        business_config = config_record.config_data if config_record else {
            "business_name": "Generic Corporate Shell",
            "industry": "Consulting Services",
            "primary_goal": "Drive discovery call bookings",
            "primary_cta": "https://calendly.com/mos-demo",
            "tone": "Professional English",
            "products": [{"name": "AI Solutions Automation Pack", "price": "$1500"}],
            "qualification_questions": ["What is your target timeline?", "What is your budget range?"],
            "objection_handling": [{"objection": "Too expensive", "response": "Highlight long-term ROI metrics."}],
            "do_not_say": ["free trials forever"]
        }

        # 2. Assert Customer, Conversation and Pipeline Session States
        customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not customer:
            customer = models.Customer(id=customer_id, tenant_id=tenant_id, name="Valued Prospect")
            db.add(customer)

        conversation = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
        if not conversation:
            conversation = models.Conversation(id=conversation_id, customer_id=customer_id, status="active")
            db.add(conversation)
            db.commit()

        # 3. Log Incoming Customer Message Turn to DB
        user_turn = models.ConversationTurn(
            conversation_id=conversation_id,
            role="user",
            message=customer_message
        )
        db.add(user_turn)
        db.commit()

        # 4. Reconstruct Recent History payload stack for context delivery
        turns_history = db.query(models.ConversationTurn).filter(
            models.ConversationTurn.conversation_id == conversation_id
        ).order_by(models.ConversationTurn.id.asc()).all()
        
        conversation_history = [
            {"role": t.role, "message": t.message} for t in turns_history
        ]

        lead_context = {
            "source": "integrated_chat_widget",
            "customer_id": customer_id,
            "conversation_id": conversation_id
        }

        agent_input = {
            "tenant_id": tenant_id,
            "customer_message": customer_message,
            "business_config": business_config,
            "lead_context": lead_context,
            "conversation_history": conversation_history[:-1]
        }

        # 5. EXECUTE AGENT STEP 1: Analytics AI
        try:
            analytics_res = AnalyticsAgent.run(agent_input)
            # Python 3.9 strict conversion guard
            if isinstance(analytics_res, str):
                analytics_res = json.loads(analytics_res)
            elif not isinstance(analytics_res, dict):
                analytics_res = dict(analytics_res)
        except Exception as err:
            analytics_res = {
                "agent": "analytics_ai", "score": 50, "intent": "unknown", 
                "category": "warm_lead", "recommended_action": "sales_followup", "error": str(err)
            }

        # 6. Synchronize Lead Table parameters based on Analytics findings
        lead = db.query(models.Lead).filter(
            models.Lead.tenant_id == tenant_id, models.Lead.customer_id == customer_id
        ).first()
        
        if not lead:
            lead = models.Lead(tenant_id=tenant_id, customer_id=customer_id)
            db.add(lead)
            
        lead.score = int(analytics_res.get("score", 50))
        lead.intent = str(analytics_res.get("intent", "general_query"))
        lead.category = str(analytics_res.get("category", "warm_lead"))
        db.commit()

        # Log Analytics output block (Convert dictionary to raw primitive string if JSON column fails on Python 3.9)
        try:
            analytics_log = models.AgentOutput(
                turn_id=user_turn.id,
                agent_name="analytics_ai",
                structured_data=analytics_res
            )
            db.add(analytics_log)
            db.commit()
        except Exception:
            db.rollback()
            analytics_log = models.AgentOutput(
                turn_id=user_turn.id,
                agent_name="analytics_ai",
                structured_data={"raw_fallback": str(analytics_res)}
            )
            db.add(analytics_log)
            db.commit()

        # Update input payload before Sales step
        agent_input["lead_context"]["analytics"] = analytics_res
        agent_input["conversation_history"] = conversation_history

        # 7. EXECUTE AGENT STEP 2: Sales AI
        try:
            sales_res = SalesAgent.run(agent_input)
            if isinstance(sales_res, str):
                sales_res = json.loads(sales_res)
            elif not isinstance(sales_res, dict):
                sales_res = dict(sales_res)
            response_text = sales_res.get("response_text", "Thank you for reaching out.")
        except Exception as err:
            sales_res = {"agent": "sales_ai", "response_text": "System processing request.", "error": str(err)}
            response_text = sales_res["response_text"]

        # 8. Log Outgoing Assistant Message Turn and JSON logs to DB
        assistant_turn = models.ConversationTurn(
            conversation_id=conversation_id,
            role="assistant",
            message=response_text
        )
        db.add(assistant_turn)
        db.commit()

        try:
            sales_log = models.AgentOutput(
                turn_id=assistant_turn.id,
                agent_name="sales_ai",
                structured_data=sales_res
            )
            db.add(sales_log)
            db.commit()
        except Exception:
            db.rollback()
            sales_log = models.AgentOutput(
                turn_id=assistant_turn.id,
                agent_name="sales_ai",
                structured_data={"raw_fallback": str(sales_res)}
            )
            db.add(sales_log)
            db.commit()

        return {
            "conversation_id": conversation_id,
            "response_text": response_text,
            "agent": "sales_ai",
            "intent": lead.intent,
            "analytics": {
                "score": lead.score,
                "category": lead.category,
                "recommended_action": str(analytics_res.get("recommended_action", "sales_followup"))
            }
        }