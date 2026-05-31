# docs/stories/phase1_stories.md

# Phase 1 Stories — MOS

---

# STORY-001 — Business Config Creation

## Owner Role

Backend Engineer

---

## Goal

As an admin,
I can create a business config,
so that AI agents behave according to that business.

---

## Acceptance Criteria

* POST /config/create works
* config stored in DB
* config retrievable
* validation exists

---

## Dependencies

* DB setup
* config schema

---

# STORY-002 — Lead Submission

## Owner Role

Backend Engineer

---

## Goal

As a business,
I can submit a lead,
so the system can process it.

---

## Acceptance Criteria

* POST /leads/create works
* lead stored in DB
* lead linked to tenant

---

## Dependencies

* config system
* lead schema

---

# STORY-003 — Analytics AI

## Owner Role

AI Agent Engineer

---

## Goal

As a business,
I want incoming leads scored and categorized,
so that high-quality leads are prioritized.

---

## Acceptance Criteria

* score generated
* intent detected
* category returned
* output follows agent contract

---

## Dependencies

* orchestrator
* lead API

---

# STORY-004 — Sales AI

## Owner Role

AI Agent Engineer

---

## Goal

As a business,
I want AI-generated sales responses,
so leads can move toward conversion.

---

## Acceptance Criteria

* response generated
* next action generated
* uses business config
* follows output schema

---

## Dependencies

* llm_service
* agent contract
* business config

---

# STORY-005 — Conversation Logging

## Owner Role

Backend Engineer

---

## Goal

As a system,
I want all conversations logged,
so that reporting and learning are possible.

---

## Acceptance Criteria

* messages stored
* intents stored
* timestamps stored
* AI outputs stored

---

## Dependencies

* conversations table
* orchestrator

---

# STORY-006 — Manager Summary

## Owner Role

AI Agent Engineer

---

## Goal

As a business owner,
I want summary reports,
so that I understand lead activity and system performance.

---

## Acceptance Criteria

* summary generated
* total leads shown
* top intents shown
* recommendations shown

---

## Dependencies

* logging
* analytics outputs

---

# STORY-007 — Scenario Engine

## Owner Role

AI Agent Engineer

---

## Goal

As a system,
I want to detect patterns and recurring objections,
so that workflows can improve over time.

---

## Acceptance Criteria

* detects repeated patterns
* generates recommendations
* stores updates

---

## Dependencies

* conversation logs
* agent outputs
