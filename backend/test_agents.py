# backend/test_agents.py
import json
import os

from dotenv import load_dotenv

from app.agents.analytics.analytics_agent import AnalyticsAgent
from app.agents.sales.sales_agent import SalesAgent
from app.schemas.chat_schema import ChatMessageRequest
from app.services.orchestrator.orchestrator_service import OrchestratorService

load_dotenv()


def run_local_agent_test():
    print("=" * 60)
    print("[start] MULTI-AGENT TERMINAL SMOKE TEST")
    print("=" * 60)

    if not os.getenv("GEMINI_API_KEY"):
        print("[error] GEMINI_API_KEY env variable is missing.")
        print("        Set it in backend/.env or in the shell before running.")
        return

    mock_business_config = {
        "business_name": "SaaSify Automations",
        "industry": "Software & AI Consulting",
        "primary_goal": "Get users to book an implementation discovery call",
        "primary_cta": "https://calendly.com/saasify-demo/15min",
        "tone": "Professional yet friendly English mixed with light business terms",
        "products": [
            {"name": "Custom AI Chatbot Integration", "price": "$1,500 setup fee"}
        ],
        "qualification_questions": [
            "What is your current monthly lead volume?",
            "What CRM platform do you currently use?",
        ],
        "objection_handling": [
            {
                "objection": "Too expensive",
                "response": "Explain that our setup pays for itself by converting hidden leads within 30 days.",
            }
        ],
        "do_not_say": ["guaranteed 100% conversion", "free trials forever"],
    }

    base_input = {
        "tenant_id": "tenant_saasify_99",
        "customer_message": (
            "Hey! I keep missing out on web leads outside business hours. "
            "Can your bot solve this and how much does it cost?"
        ),
        "business_config": mock_business_config,
        "lead_context": {
            "source": "website_contact_form",
            "lead_name": "Rajesh Kumar",
        },
        "conversation_history": [],
    }

    # --- STEP 1: ANALYTICS AGENT (direct) ---
    print("\n[step 1] AnalyticsAgent (direct call)")
    analytics_output = AnalyticsAgent.run(base_input)
    print(json.dumps(analytics_output, indent=2, ensure_ascii=False))

    if not analytics_output.get("success"):
        print("[abort] analytics failed — skipping remaining steps.")
        return

    # --- STEP 2: SALES AGENT (direct, with analytics signal merged) ---
    print("\n[step 2] SalesAgent (direct call, analytics signal injected)")
    sales_input = dict(base_input)
    sales_input["analytics_signal"] = analytics_output.get("data")
    sales_input["conversation_history"] = [
        {"role": "user", "message": base_input["customer_message"]}
    ]
    sales_output = SalesAgent.run(sales_input)
    print(json.dumps(sales_output, indent=2, ensure_ascii=False))

    # --- STEP 3: ORCHESTRATOR (full Phase 1 pipeline) ---
    print("\n[step 3] OrchestratorService.process_chat_message (full pipeline)")
    chat_payload = ChatMessageRequest(
        tenant_id="tenant_saasify_99",
        conversation_id="conv_001",
        message=base_input["customer_message"],
        lead_context=base_input["lead_context"],
        conversation_history=[],
        business_config_override=mock_business_config,
    )
    orchestrator_output = OrchestratorService.process_chat_message(chat_payload)
    print(json.dumps(orchestrator_output, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print("[done] all paths executed.")
    print("=" * 60)


if __name__ == "__main__":
    run_local_agent_test()
