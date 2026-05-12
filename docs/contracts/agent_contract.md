# docs/contracts/agent_contract.md

# Agent Contract — MOS Phase 1

## Purpose

Defines standardized communication format for all AI agents.

This contract is mandatory for:

* Analytics AI
* Sales AI
* Support AI
* Scenario Engine
* Manager AI

---

# Common Rules

## Rules

* All outputs must be JSON-compatible.
* No freeform unpredictable outputs.
* No direct DB access from agents.
* Agents communicate through services/orchestrator.
* Agents must remain modular and replaceable.

---

# Common Agent Input

```json
{
  "tenant_id": "demo_business",
  "conversation_id": "conv_001",
  "customer_message": "price kya hai?",
  "business_config": {},
  "lead_context": {},
  "conversation_history": []
}
```

---

# Common Agent Output

```json
{
  "agent": "sales_ai",
  "intent": "pricing_query",
  "response_text": "Bilkul, main help karta hoon.",
  "next_action": "ask_need",
  "confidence": 0.85,
  "tags": ["pricing", "qualification"]
}
```

---

# Analytics AI Contract

## Responsibilities

* lead scoring
* intent detection
* lead categorization

---

## Output Example

```json
{
  "agent": "analytics_ai",
  "score": 82,
  "intent": "pricing_query",
  "category": "hot_lead",
  "recommended_action": "sales_followup"
}
```

---

# Sales AI Contract

## Responsibilities

* qualification
* objection handling
* CTA generation

---

## Output Example

```json
{
  "agent": "sales_ai",
  "response_text": "Aapka budget range kya hai?",
  "next_action": "collect_budget",
  "intent": "qualification",
  "confidence": 0.91
}
```

---

# Support AI Contract

## Responsibilities

* issue resolution
* FAQ handling
* escalation detection

---

## Output Example

```json
{
  "agent": "support_ai",
  "response_text": "Main aapki help karta hoon.",
  "issue_type": "refund",
  "escalation_required": false
}
```

---

# Scenario Engine Contract

## Responsibilities

* pattern detection
* scenario identification
* recommendation generation

---

## Output Example

```json
{
  "agent": "scenario_engine",
  "patterns_detected": [
    "pricing objection"
  ],
  "recommendations": [
    "improve pricing explanation"
  ]
}
```

---

# Manager AI Contract

## Responsibilities

* summaries
* reporting
* business insights

---

## Output Example

```json
{
  "agent": "manager_ai",
  "summary": {
    "total_leads": 12,
    "hot_leads": 5
  },
  "recommendations": [
    "increase Instagram campaigns"
  ]
}
```

---

# Important Engineering Rule

Agents must NEVER:

* redesign architecture
* bypass orchestrator
* directly access frontend
* tightly couple with services

All orchestration must happen through backend services.
