import json
from app.services.llm.llm_service import generate_json_response


class SalesAgent:
    @staticmethod
    def run(agent_input: dict) -> dict:
        """
        Conversation and persuasion engine.
        Responsibilities: qualification, conversation, objection handling, CTA generation, follow-up direction.
        The goal is not just answering, but moving the lead toward action.
        """
        tenant_id = agent_input.get("tenant_id", "unknown")
        customer_message = agent_input.get("customer_message", "")
        business_config = agent_input.get("business_config", {})
        lead_context = agent_input.get("lead_context", {})
        conversation_history = agent_input.get("conversation_history", [])

        # Format business-specific parameters dynamically to ensure no hardcoding
        tone = business_config.get("tone", "Professional English")
        primary_goal = business_config.get("primary_goal", "")
        primary_cta = business_config.get("primary_cta", "")
        products = business_config.get("products", [])
        faqs = business_config.get("faqs", [])
        qualification_questions = business_config.get("qualification_questions", [])
        objection_handling = business_config.get("objection_handling", [])
        do_not_say = business_config.get("do_not_say", [])

        system_instruction = f"""
You are the Sales AI agent for a Multi-Agent Operating System (MOS).
Your purpose is to drive conversions and guide the lead through the qualification pipeline.

Responsibilities:
- Conduct qualification conversations naturally based on the missing answers in your qualification list.
- Handle objections smoothly using the provided guidelines.
- Proactively guide the lead toward the primary CTA: "{primary_cta}".
- Keep responses fully personalized to the lead context.

Business Configuration Rules for Tenant '{tenant_id}':
- Business Name: {business_config.get('business_name', 'N/A')}
- Industry: {business_config.get('industry', 'N/A')}
- Communication Tone: {tone}
- Primary Goal: {primary_goal}
- Products/Services: {json.dumps(products)}
- Reference FAQs: {json.dumps(faqs)}
- Questions to Qualify Lead: {json.dumps(qualification_questions)}
- Objection Handling Guidelines: {json.dumps(objection_handling)}
- Restricted Phrases (DO NOT SAY): {json.dumps(do_not_say)}

Core Persuasion Principle: Do not simply answer questions passively. Use your answers to move the user toward the next step of qualification or the primary call-to-action. Always respond natively in the requested tone ({tone}).

Strict Rule: You must return ONLY valid JSON matching the requested schema. Do not include markdown code fences or conversational text wrapper blocks.
""".strip()

        user_prompt = f"""
Lead Info:
{json.dumps(lead_context, indent=2)}

Full Conversation History:
{json.dumps(conversation_history, indent=2)}

Incoming Customer Message:
"{customer_message}"

Generate the appropriate sales response and fill out the metadata schema.
""".strip()

        expected_schema = """
{
  "agent": "sales_ai",
  "response_text": "Aapka budget range kya hai?",
  "next_action": "collect_budget",
  "intent": "qualification",
  "confidence": 0.91
}
""".strip()

        return generate_json_response(
            system_instruction=system_instruction,
            user_prompt=user_prompt,
            expected_schema=expected_schema,
            temperature=0.3
        )