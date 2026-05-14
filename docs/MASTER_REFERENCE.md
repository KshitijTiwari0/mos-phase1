# MASTER_REFERENCE.md
# Architecture Version: 1.1

# MOS Phase 1 — Master Reference Document

## 1. Project Overview

### Project Name

c

### Product Definition

MOS is a configurable AI workforce system for businesses.

The system is designed to:

* capture and analyze leads
* converse with leads
* qualify and persuade leads
* generate support responses
* monitor business interactions
* detect patterns from conversations
* generate business insights and reports

This is NOT:

* a chatbot builder
* a workflow automation-only tool
* a single-purpose sales bot

This IS:

* a configurable multi-agent business operating system

---

# 2. Core Philosophy

## Important Principles

### 1. Same Codebase, Different Businesses

The codebase remains generic.

Business-specific behavior comes from:

* business config
* prompts
* knowledge base
* rules
* FAQs
* tone
* objectives

NOT from changing code.

---

### 2. Backend is the Brain

The backend controls:

* decision making
* orchestration
* memory
* routing
* learning
* logging

n8n is NOT the brain.

n8n is only:

* automation layer
* integration layer
* webhook layer

---

### 3. Agents are Modular

Every agent must:

* have fixed input/output contracts
* be independently replaceable
* not directly depend on frontend
* not tightly couple with other agents

---

### 4. Contract-First Development

Before implementation:

* API contracts
* DB schema
* agent schemas
* orchestration rules

must be frozen.

---

### 5. Config-Driven Architecture

Never hardcode business logic.

Bad:

```python
if business == "coaching":
```

Good:

```python
config["qualification_questions"]
```

---

# 3. High-Level System Architecture

```text
Frontend Dashboard
        ↓
Backend API Layer (FastAPI)
        ↓
Orchestrator Service
        ↓
Business Config Loader
        ↓
AI Agents
 ├── Analytics AI
 ├── Sales AI
 ├── Support AI
 ├── Scenario Update Engine
 └── Manager AI
        ↓
Database + Memory Layer
        ↓
Integration Layer (n8n)
 ├── WhatsApp
 ├── Google Sheets
 ├── CRM
 ├── Email
 └── Scheduling
```

---

# 4. Core Components

## 4.1 Frontend

### Responsibilities

* business config form
* lead dashboard
* conversation viewer
* reports dashboard
* scenario updates display

### Tech

* React / Next.js
* Tailwind CSS

---

## 4.2 Backend API Layer

### Responsibilities

* receive requests
* validate payloads
* auth
* orchestration entrypoint
* expose APIs

### Tech

* FastAPI
* Pydantic

---

## 4.3 Orchestrator Service

### Purpose

Controls workflow routing.

### Responsibilities

* decide which agent runs
* manage workflow execution
* coordinate agents
* trigger logging
* trigger reports
* trigger scenario analysis

### Important

Orchestrator is NOT an AI agent.

It is a backend controller/router.

---

## 4.4 Analytics AI

### Purpose

Lead analysis and categorization.

### Responsibilities

* source analysis
* lead scoring
* lead categorization
* urgency detection
* route recommendation

### Output

* score
* intent
* category
* recommended action

---

## 4.5 Sales AI

### Purpose

Conversation and persuasion engine.

### Responsibilities

* qualification
* conversation
* objection handling
* CTA generation
* follow-up direction

### Important

Sales AI is the main differentiator.

The goal is not answering.
The goal is moving the lead toward action.

---

## 4.6 Support AI

### Purpose

Customer support handling.

### Responsibilities

* issue identification
* FAQ handling
* complaint logging
* escalation detection

---

## 4.7 Scenario Update Engine

### Purpose

Learning and pattern detection.

### Responsibilities

* identify repeated patterns
* detect new objections
* detect failure cases
* suggest improvements
* generate scenario updates

### Inputs

* transcripts
* conversation logs
* support logs
* outcomes

### Outputs

* new FAQ suggestions
* prompt improvement suggestions
* scenario reports

---

## 4.8 Manager AI

### Purpose

Business-level monitoring and reporting.

### Responsibilities

* summarize activity
* identify gaps
* generate reports
* suggest improvements
* monitor system quality

### Important

Manager AI is NOT the orchestrator.

Manager AI is:

* business intelligence
* reporting
* supervision

---

# 5. Business Config System

## Purpose

Allows the same codebase to work for different businesses.

---

## Business Config Example

```json
{
  "business_name": "Demo Business",
  "industry": "Education",
  "tone": "Friendly Hinglish",
  "primary_goal": "Book demo class",
  "products": [],
  "faqs": [],
  "qualification_questions": [],
  "objection_handling": [],
  "primary_cta": "Book appointment",
  "escalation_rules": [],
  "do_not_say": []
}
```

---

## Business Config Responsibilities

Defines:

* tone
* goals
* products
* FAQs
* CTAs
* escalation rules
* qualification questions
* objection handling

---

# 6. Tech Stack

## Backend

* Python
* FastAPI
* Pydantic

## Database

* PostgreSQL

## Session Memory

* Redis

## Background Jobs

* Celery or RQ

## Vector Storage

* pgvector

## AI

Current Phase 1:
- Google Gemini API
- Google GenAI SDK
- Centralized llm_service

Future:
- OpenRouter/OpenAI-compatible provider abstraction
- Agent-specific model routing

## Frontend

* React / Next.js
* Tailwind

## Automation

* n8n

## Deployment

* Docker

---

# 7. Folder Structure

```text
mos-phase1/

  backend/
    app/
      api/
      agents/
        analytics/
        sales/
        support/
        scenario/
        manager/
      services/
        orchestrator/
        config/
        memory/
        llm/
        reports/
        integrations/
      db/
        models/
        migrations/
      prompts/
      workers/
      main.py

  frontend/
    app/
      dashboard/
      config/
      leads/
      conversations/
      reports/

  workflows/
    n8n/

  docs/
    architecture/
    contracts/
    stories/

  docker-compose.yml
  README.md
```

---

# 8. Agent Input/Output Contract

## Common Agent Input

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

## Common Agent Output

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

# 9. API Contracts

## Config APIs

```text
POST /config/create
GET  /config/{tenant_id}
```

---

## Lead APIs

```text
POST /leads/create
GET  /leads/{tenant_id}
```

---

## Chat APIs

```text
POST /chat/message
```

---

## Reports APIs

```text
POST /reports/generate
GET  /reports/{tenant_id}
```

---

## Scenario APIs

```text
POST /scenario/analyze
GET  /scenario/{tenant_id}
```

---

# 10. Database Tables

```text
tenants
business_configs
customers
leads
conversations
conversation_turns
agent_outputs
scenario_updates
manager_reports
```

---

# 11. Orchestrator Rules

## Initial Rule-Based Routing

```text
new_lead → Analytics AI

pricing / interested / demo
→ Sales AI

complaint / support / refund
→ Support AI

conversation_complete
→ Scenario Engine

daily_report
→ Manager AI
```

---

# 12. Data Flow

## Lead Flow

```text
Lead Arrives
→ Orchestrator
→ Analytics AI
→ Sales AI
→ Conversation Log
→ Scenario Engine
→ Manager Report
```

---

## Support Flow

```text
Customer Query
→ Orchestrator
→ Support AI
→ Support Log
→ Scenario Engine
→ Manager Report
```

---

# 13. Logging Rules

Everything must be logged.

Must store:

* customer messages
* AI responses
* detected intent
* objection tags
* scores
* outcomes
* timestamps

---

# 14. Memory System

## Short-Term Memory

Stored in Redis.

Contains:

* recent conversation
* active intent
* unresolved objections

---

## Long-Term Memory

Stored in PostgreSQL.

Contains:

* lead history
* support history
* summaries
* previous outcomes

---

# 15. Role Structure

## 1. Solution Architect

Responsibilities:

* architecture
* boundaries
* contracts
* workflows

---

## 2. Backend Engineer

Responsibilities:

* APIs
* DB
* orchestrator
* services

---

## 3. AI Agent Engineer

Responsibilities:

* prompts
* agent logic
* response quality
* evaluation

---

## 4. Integration Engineer

Responsibilities:

* n8n
* webhooks
* CRM
* Sheets
* scheduling

---

## 5. Product / Workflow Owner

Responsibilities:

* stories
* acceptance criteria
* milestones
* demo flow

---

# 16. Coding Principles

## 1. Never hardcode business behavior

---

## 2. All agents must follow contracts

---

## 3. Use service layers

Bad:

```python
sales_agent -> direct DB query
```

Good:

```python
sales_agent -> conversation_service
```

---

## 4. Modular architecture only

Agents should be independently replaceable.

---

## 5. JSON-first outputs

All agent outputs should be structured.

---
## 6. LLM Access Rule

All LLM communication must happen through:
services/llm/llm_service.py

Agents must never directly call providers.

# 17. Phase 1 Demo Scope

## Included

* business config creation
* manual lead submission
* Analytics AI scoring
* Sales AI first response
* conversation logging
* Manager summary

---

## Excluded

* live calling
* full WhatsApp integration
* payment
* enterprise CRM sync
* autonomous learning
* advanced memory systems

---

# 18. Phase 1 Stories

## STORY-001

Business Config Creation

---

## STORY-002

Lead Submission + Analytics AI

---

## STORY-003

Sales AI Response Generation

---

## STORY-004

Conversation Logging

---

## STORY-005

Scenario Detection

---

## STORY-006

Manager Summary Report

---

# 19. Team Workflow

## Development Style

Use:

* mini agile
* vertical slices
* contract-first development

Avoid:

* random coding
* architecture drift
* tightly coupled modules

---

## Recommended Workflow

```text
Architecture
→ Contracts
→ Stories
→ APIs
→ Agents
→ Integrations
→ Frontend
```

---

# 20. ChatGPT Workflow Strategy

## Master Chat

Purpose:

* architecture
* decisions
* source of truth

---

## Backend Chat

Purpose:

* APIs
* DB
* services

---

## AI Engineer Chat

Purpose:

* prompts
* agent logic
* evaluation

---

## Integration Chat

Purpose:

* n8n
* webhooks
* Sheets
* CRM

---

## Product Chat

Purpose:

* stories
* roadmap
* milestones

---

# 21. Important Clarifications

## n8n is NOT the brain

n8n is:

* integration
* automation
* workflow helper

The backend is the brain.

---

## Orchestrator is NOT Manager AI

Orchestrator:

* routing
* execution control

Manager AI:

* reporting
* monitoring
* suggestions

---

## This system is NOT use-case-specific

It is:

* configurable
* multi-business
* config-driven

---

# 22. Future Scope (Phase 2+)

Potential additions:

* autonomous prompt optimization
* cross-business learning
* predictive lead scoring
* voice calling
* CRM intelligence
* advanced memory
* evaluation systems
* self-improving workflows

---

# 23. Final Project Vision

MOS is intended to become a reusable AI business operating system where businesses can plug in:

* their products
* FAQs
* tone
* goals
* rules

and instantly deploy:

* AI sales workflows
* AI support workflows
* analytics
* reporting
* learning systems

without rewriting the core codebase.
