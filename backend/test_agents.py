# backend/test_agents.py
import os
import json
from app.agents.analytics.analytics_agent import AnalyticsAgent
from app.agents.sales.sales_agent import SalesAgent

def run_local_agent_test():
    print("=" * 60)
    print("🚀 STARTING MULTI-AGENT TERMINAL SMOKE TEST...")
    print("=" * 60)

    # 1. Verify environment variable is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: 'GEMINI_API_KEY' environment variable is missing!")
        print("Please export it in your terminal before running this script.")
        return

    # 2. Mock up a realistic business configuration contract
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
            "What CRM platform do you currently use?"
        ],
        "objection_handling": [
            {"objection": "Too expensive", "response": "Explain that our setup pays for itself by converting hidden leads within 30 days."}
        ],
        "do_not_say": ["guaranteed 100% conversion", "free trials forever"]
    }

    # 3. Create initial incoming pipeline data mock
    agent_input = {
        "tenant_id": "tenant_saasify_99",
        "customer_message": "Hey! I keep missing out on web leads outside business hours. Can your bot solve this and how much does it cost?",
        "business_config": mock_business_config,
        "lead_context": {
            "source": "website_contact_form",
            "lead_name": "Rajesh Kumar"
        },
        "conversation_history": []
    }

    # --- TEST 1: ANALYTICS AGENT ---
    print("\n[Step 1] Invoking AnalyticsAgent...")
    try:
        analytics_output = AnalyticsAgent.run(agent_input)
        print("✅ AnalyticsAgent Response Received Object:")
        print(json.dumps(analytics_output, indent=2))
    except Exception as e:
        print(f"❌ AnalyticsAgent crashed with exception: {e}")
        return

    # --- TEST 2: SALES AGENT ---
    print("\n[Step 2] Invoking SalesAgent...")
    # Add a conversational turn record into history to mimic the pipeline progression
    agent_input["conversation_history"].append({
        "role": "user",
        "message": agent_input["customer_message"]
    })
    
    try:
        sales_output = SalesAgent.run(agent_input)
        print("✅ SalesAgent Response Received Object:")
        print(json.dumps(sales_output, indent=2))
    except Exception as e:
        print(f"❌ SalesAgent crashed with exception: {e}")
        return

    print("\n" + "=" * 60)
    print("🎉 ALL AGENTS EXECUTED SUCCESSFULLY AND RETURNED CLEAN STRUCTURAL JSON!")
    print("=" * 60)

if __name__ == "__main__":
    run_local_agent_test()