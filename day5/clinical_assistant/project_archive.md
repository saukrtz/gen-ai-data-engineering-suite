# 📚 Clinical Data Assistant: Master Project Archive

This document serves as the comprehensive record of the AI-Powered Clinical Data Assistant project, developed on May 4, 2026.

---

## 1. Project Vision & Goals
**Objective**: Build a secure, agentic clinical assistant that allows doctors to query patient data using natural language.
**Core Philosophy**: 
- **Local-First**: Fast performance without heavy frameworks.
- **MCP-Inspired**: Modular tool-calling architecture.
- **Clinical Grade**: Built-in security (SQL Guardian) and privacy (PII Masking).

---

## 2. Technical Stack
- **LLM**: Groq Llama-3.1-8b-instant (Primary reasoning engine).
- **Backend**: FastAPI (Python-based tool gateway).
- **Database**: Snowflake (Clinical Data Warehouse).
- **Environment**: Python 3.9+, `.env` for secrets management.

---

## 3. The 5-Phase Implementation
We completed the project in five distinct, focused phases:

### Phase 1: Architecture & Scaffolding
- Established the directory structure.
- Configured the Antigravity Agent for autonomous file management.
- Initialized the FastAPI server foundation.

### Phase 2: Data Engineering
- Modeled the Snowflake Clinical Schema:
    - `PATIENTS`: `patient_id`, `name`, `age`, `gender`, `diagnosis`.
    - `ADMISSIONS`: `admission_id`, `patient_id`, `admission_date`, `discharge_date`, `department`.
    - `VITALS`: `patient_id`, `bp`, `heart_rate`, `recorded_at`.

### Phase 3: Tool Execution Layer
- Developed three modular tools:
    - **`sql_tool.py`**: Executes complex clinical joins and analytical queries.
    - **`drug_tool.py`**: A simulated clinical database for safety checks.
    - **`file_tool.py`**: Dynamic path-aware reader for unstructured guidelines.
- Integrated all tools into the `main.py` FastAPI server.

### Phase 4: Intelligence & Routing
- Built the **Agent Brain** (`agent.py`).
- Implemented **Strict Routing**: The LLM analyzes queries and maps them to JSON tool-call instructions.
- Added **Synthesized Summarization**: The LLM takes raw JSON data and converts it into professional clinical reports.

### Phase 5: Security & Governance
- **SQL Guardian**: Interceptor logic that regex-scans for destructive keywords (`DROP`, `DELETE`, etc.).
- **PII Masking Engine**: Automatic redaction of the `NAME` column in all results to maintain HIPAA-like compliance.

---

## 4. Key Logic Documentation

### The "Brain" (Router) Logic
The agent uses a strict system prompt to classify queries. 
- *Rule*: Never send SQL to the Drug tool. 
- *Rule*: Always join on `patient_id` for SQL queries.

### The Security Interceptor
```python
def validate_query(query: str):
    forbidden = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "ALTER", "INSERT"]
    if any(cmd in query.upper() for cmd in forbidden):
        raise Exception("Security Alert: Destructive command blocked.")
```

### The PII Masking Engine
```python
def mask_pii(results):
    for row in results:
        if "NAME" in row:
            row["NAME"] = "REDACTED_PATIENT_PII"
    return results
```

---

## 5. How to Re-Run Everything
1. **Activate Environment**: Ensure `fastapi`, `snowflake-connector-python`, and `groq` are installed.
2. **Configure `.env`**: Populate with actual credentials.
3. **Start Server**: `cd app && python3 main.py`
4. **Start Agent**: `cd app && python3 agent.py`

---

## 6. Project Directory Final Map
```text
clinical_assistant/
├── README.md               # Quick-start guide
├── project_archive.md      # (This file) Full development history
├── .env                    # Credentials
├── data/                   # Clinical guideline files
└── app/
    ├── main.py             # FastAPI Gateway
    ├── agent.py            # AI Router & Brain
    ├── benchmarks.py       # Validation suite
    └── tools/
        ├── sql_tool.py     # Snowflake Logic & Security
        ├── drug_tool.py    # Medication Logic
        └── file_tool.py    # File Reader Logic
```

---
*Archive Compiled by Antigravity IDE Agent.*
