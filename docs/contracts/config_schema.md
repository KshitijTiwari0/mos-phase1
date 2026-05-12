# docs/contracts/config_schema.md

# Business Config Schema — MOS Phase 1

## Purpose

Defines configurable business behavior for AI agents.

The same codebase should support multiple businesses using this config system.

---

# Rules

* No business-specific hardcoding in code.
* All business behavior must come from config.
* Config must remain editable.
* Agents must dynamically use config values.

---

# Config Schema

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
  "primary_cta": "Book appointment",
  "escalation_rules": [],
  "do_not_say": []
}
```

---

# Field Definitions

## tenant_id

Unique identifier for business.

Example:

```text
demo_business
```

---

## business_name

Display/business name.

---

## industry

Business category.

Examples:

* Education
* Real Estate
* E-commerce
* Automotive

---

## tone

Defines communication style.

Examples:

* Friendly Hinglish
* Professional English
* Formal Hindi

---

## primary_goal

Main business objective.

Examples:

* Book demo
* Generate appointment
* Close sale
* Collect lead info

---

## products

List of products/services.

---

## faqs

Business FAQs used by agents.

---

## qualification_questions

Questions Sales AI should ask.

Examples:

* budget
* city
* requirement
* timeline

---

## objection_handling

Known objections and handling guidelines.

---

## primary_cta

Primary call-to-action.

Examples:

* Book appointment
* Schedule demo
* Share contact number

---

## escalation_rules

Conditions where human escalation is required.

---

## do_not_say

Restricted phrases or responses.

---

# Important Engineering Principle

Business behavior should change by:

* changing config
* changing prompts

NOT by:

* changing backend code
* changing APIs
