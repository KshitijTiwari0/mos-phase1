# docs/contracts/db_schema.md

# Database Schema — MOS Phase 1

## Database Choice

Current Phase 1:

* SQLite

Future:

* PostgreSQL

---

# Tables

## 1. tenants

### Purpose

Stores business/tenant information.

---

### Columns

```text
id
tenant_id
business_name
industry
created_at
```

---

# 2. business_configs

### Purpose

Stores business configuration.

---

### Columns

```text
id
tenant_id
config_json
created_at
updated_at
```

---

# 3. leads

### Purpose

Stores incoming leads.

---

### Columns

```text
id
tenant_id
name
source
message
status
created_at
```

---

# 4. conversations

### Purpose

Stores conversations.

---

### Columns

```text
id
tenant_id
conversation_id
lead_id
status
created_at
```

---

# 5. conversation_turns

### Purpose

Stores message-by-message conversation history.

---

### Columns

```text
id
conversation_id
speaker
agent_name
message
intent
timestamp
```

---

# 6. agent_outputs

### Purpose

Stores structured agent outputs.

---

### Columns

```text
id
conversation_id
agent_name
output_json
created_at
```

---

# 7. scenario_updates

### Purpose

Stores detected patterns and recommendations.

---

### Columns

```text
id
tenant_id
pattern
recommendation
created_at
```

---

# 8. manager_reports

### Purpose

Stores generated manager summaries.

---

### Columns

```text
id
tenant_id
summary_json
created_at
```

---

# Relationships

## Flow

```text
Tenant
→ Leads
→ Conversations
→ Conversation Turns
→ Agent Outputs
→ Reports
```

---

# Important Rules

## 1. No direct DB access from agents

Agents must use:

* services
* repositories
* orchestrator

---

## 2. Use JSON fields for flexibility

Examples:

* config_json
* output_json
* summary_json

---

## 3. Future Migration Support

Schema should support:

* SQLite → PostgreSQL migration
* async workers
* scaling
* analytics
