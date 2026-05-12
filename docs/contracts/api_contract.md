# docs/contracts/api_contract.md

# API Contract — MOS Phase 1

## Rules

* All APIs must return JSON.
* All APIs must be version-safe.
* No business-specific hardcoding.
* Every request must include `tenant_id`.
* APIs should remain modular and reusable.

---

# Base URL

```text
http://localhost:8000
```

---

# 1. Health Check API

## GET /health

### Response

```json
{
  "status": "ok",
  "service": "mos-phase1-backend"
}
```

---

# 2. Create Business Config

## POST /config/create

### Purpose

Creates business configuration used by AI agents.

---

### Request Body

```json
{
  "tenant_id": "demo_business",
  "business_name": "Demo Business",
  "industry": "Education",
  "tone": "Friendly Hinglish",
  "primary_goal": "Book demo class",
  "products": [],
  "faqs": [],
  "qualification_questions": [],
  "objection_handling": [],
  "primary_cta": "Book appointment"
}
```

---

### Response

```json
{
  "success": true,
  "tenant_id": "demo_business"
}
```

---

# 3. Get Business Config

## GET /config/{tenant_id}

### Response

```json
{
  "tenant_id": "demo_business",
  "business_name": "Demo Business",
  "industry": "Education"
}
```

---

# 4. Create Lead

## POST /leads/create

### Purpose

Submits a new lead into the system.

---

### Request Body

```json
{
  "tenant_id": "demo_business",
  "name": "Rohan",
  "source": "Instagram",
  "message": "price kya hai?"
}
```

---

### Response

```json
{
  "lead_id": "lead_001",
  "status": "received"
}
```

---

# 5. Chat Message API

## POST /chat/message

### Purpose

Processes incoming customer messages.

---

### Request Body

```json
{
  "tenant_id": "demo_business",
  "conversation_id": "conv_001",
  "message": "price kya hai?"
}
```

---

### Response

```json
{
  "response_text": "Bilkul, main help karta hoon.",
  "agent": "sales_ai",
  "intent": "pricing_query"
}
```

---

# 6. Generate Reports

## POST /reports/generate

### Purpose

Generates manager summary report.

---

### Request Body

```json
{
  "tenant_id": "demo_business"
}
```

---

### Response

```json
{
  "summary": {
    "total_leads": 10,
    "hot_leads": 4
  }
}
```

---

# 7. Scenario Analysis

## POST /scenario/analyze

### Purpose

Runs scenario analysis on conversations.

---

### Request Body

```json
{
  "tenant_id": "demo_business"
}
```

---

### Response

```json
{
  "patterns_detected": [],
  "recommendations": []
}
```

---

# Important Notes

## API Stability

Once contracts are frozen:

* implementation must follow contracts
* architecture changes should happen in architect chat only

---

## Error Handling

Standard format:

```json
{
  "success": false,
  "error": "error_message"
}
```

---

## Future Additions

Planned:

* authentication
* role-based access
* async processing
* pagination
* webhooks
* streaming responses
