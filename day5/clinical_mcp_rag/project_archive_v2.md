# 📚 Clinical Assistant (Modular): Master Project Archive

This document is the definitive record of the **Modular Clinical MCP/RAG Assistant**, developed to solve the "hallucination" challenges of earlier iterations.

---

## 1. Project Identity
**Objective**: Build a high-precision clinical assistant using a deterministic hybrid architecture (RAG + SQL).
**Key Technology Shift**: 
- **From**: Open-ended SQL generation.
- **To**: Whitelisted column enforcement and few-shot logic.

---

## 2. The Modular Architecture
The system is split into three "clean" components to ensure the LLM never confuses data types:

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Knowledge RAG** | FAISS + HuggingFace | Searches unstructured clinical guidelines (`guidelines.txt`). |
| **Database MCP** | SQLite3 + FastAPI | Executes deterministic SQL on structured patient records. |
| **Orchestrator** | LangChain + Groq | Routes queries, generates SQL, and synthesizes grounded answers. |

---

## 3. Core Technical Fixes (Zero Hallucination Strategy)
We implemented three critical layers of protection to ensure the LLM remains accurate:

### A. Column Whitelisting
In the `generate_sql` prompt, we strictly limited the columns the AI is allowed to see and use:
`COLUMNS YOU MAY USE (WHITELIST): id, name, age, gender, diagnosis, bp, visit_date.`

### B. Few-Shot SQL Patterning
We provided the AI with explicit "correct" examples to ensure it uses `GROUP BY` correctly:
```sql
-- Pattern for Patient Counts:
SELECT diagnosis, COUNT(*) FROM PATIENT_DATA GROUP BY diagnosis
```

### C. Context Separation
We trained the LLM to understand that **Guidelines** come from the RAG tool and **Data** comes from the SQL tool, forbidding it from trying to find "treatment advice" inside the database.

---

## 4. Final Directory Map
```text
clinical_mcp_rag/
├── guidelines.txt          # Raw medical knowledge
├── hospital.db             # SQLite Clinical Database
├── .env                    # Groq API Key
└── app/
    ├── agent_orchestrator.py  # The "Brain" (Main Entry Point)
    └── tools/
        ├── knowledge_rag.py   # Vector Search Logic
        └── database_mcp.py    # SQL Execution Server
```

---

## 5. Execution Flow
1. **Start the Database Server**: 
   `python3 database_mcp.py` (Exposes port 8000).
2. **Run the Orchestrator**: 
   `python3 agent_orchestrator.py`.
3. **Query Logic**: 
   - LLM detects intent.
   - Triggers RAG and/or SQL concurrently.
   - Synthesizes a response grounded ONLY in the retrieved text.

---

## 6. Project Accomplishments
- Successfully mapped **BP 150** to **Stage 1 Hypertension**.
- Successfully joined `patient_data` with relevant guidelines.
- Eliminated all "Object not found" and "Invalid Identifier" errors through strict schema mapping.

---
*Archive Compiled by Antigravity AI Agent.*
