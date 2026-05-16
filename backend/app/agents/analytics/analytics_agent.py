import json
from app.services.llm.llm_service import generate_json_response


class AnalyticsAgent:
    @staticmethod
    def run(agent_input: dict) -> dict:
        """
        Lead analysis and categorization agent.
        Responsibilities: source analysis, lead scoring, lead categorization, urgency detection, route recommendation.
        """
        tenant_id = agent_input.get("tenant_id", "unknown")
        customer_message = agent_input.get("customer_message", "")
        business_config = agent_input.get("business_config", {})
        lead_context = agent_input.get("lead_context", {})
        conversation_history = agent_input.get("conversation_history", [])

        system_instruction = f"""
You are the Analytics AI agent for a Multi-Agent Operating System (MOS).
Your purpose is to perform lead analysis, intent detection, and lead categorization.

Responsibilities:
1. Analyze the incoming customer message and lead context (source, name, etc.).
2. Evaluate lead quality and assign a score between 0 and 100 based on alignment with the business primary goals and products.
3. Detect the customer's intent and categorize the lead (e.g., hot_lead, warm_lead, cold_lead).
4. Recommend the next workflow action (e.g., sales_followup, support_routing, ignore).

Business Context for Tenant '{tenant_id}':
- Business Name: {business_config.get('business_name', 'N/A')}
- Industry: {business_config.get('industry', 'N/A')}
- Primary Goal: {business_config.get('primary_goal', 'N/A')}
- Primary CTA: {business_config.get('primary_cta', 'N/A')}
- Qualification Criteria: {json.dumps(business_config.get('qualification_questions', []))}

Strict Rule: You must return ONLY valid JSON matching the requested schema. Do not include markdown code fences or conversational text wrapper blocks.
""".strip()

        user_prompt = f"""
Lead Context:
{json.dumps(lead_context, indent=2)}

Recent Conversation History:
{json.dumps(conversation_history, indent=2)}

Latest Customer Message:
"{customer_message}"

Analyze this interaction and populate the requested fields according to the expected schema.
""".strip()

        expected_schema = """
{
  "agent": "analytics_ai",
  "score": 82,
  "intent": "pricing_query",
  "category": "hot_lead",
  "recommended_action": "sales_followup"
}
""".strip()

        return generate_json_response(
            system_instruction=system_instruction,
            user_prompt=user_prompt,
            expected_schema=expected_schema,
            temperature=0.2
        )