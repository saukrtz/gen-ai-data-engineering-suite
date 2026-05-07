# AI-Powered Clinical Data Assistant 🏥

An agentic, local-first clinical data system designed to allow healthcare professionals to query patient data, check drug safety, and analyze clinical reports using natural language.

---

## 🏗 Architecture Overview
The system follows a **Model Context Protocol (MCP)** architecture:
- **Brain**: Groq Llama-3.1-8b-instant (Decision-making & SQL generation).
- **Gateway**: FastAPI MCP Server (Action orchestration).
- **Storage**: Snowflake (Clinical Data Warehouse).
- **Execution Agent**: Modular tool-calling system with security interception.

---

## 📁 Project Structure
```text
clinical_assistant/
├── app/
│   ├── main.py           # FastAPI Server Entry Point
│   ├── agent.py          # LLM Routing & Synthesis Logic
│   ├── benchmarks.py     # System Validation Suite
│   └── tools/
│       ├── sql_tool.py   # Snowflake connectivity & PII Masking
│       ├── drug_tool.py  # Medication safety logic
│       └── file_tool.py  # Clinical report ingestion
├── data/                 # Clinical reports & guideline storage
└── .env                  # Secure Credentials (Groq, Snowflake)
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+
- A Snowflake Account
- A Groq API Key

### 2. Dependency Installation
If you see `ModuleNotFoundError`, ensure you install the dependencies:
```bash
pip install fastapi uvicorn snowflake-connector-python requests groq python-dotenv pydantic
```

### 3. Configuration
Update the `.env` file in `gen_ai/clinical_assistant/` with your credentials:
```env
GROQ_API_KEY=gsk_...
SNOWFLAKE_USER=...
SNOWFLAKE_PASSWORD=...
SNOWFLAKE_ACCOUNT=...
SNOWFLAKE_WH=...
SNOWFLAKE_DB=CLINICAL_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

---

## 🏃 How to Run the System

1. **Start the MCP Server**:
   ```bash
   cd gen_ai/day5/clinical_assistant/app
   python3 main.py
   ```

2. **Run the Clinical Agent** (New Terminal):
   ```bash
   cd gen_ai/day5/clinical_assistant/app
   python3 agent.py
   ```

3. **Run System Benchmarks**:
   ```bash
   python3 benchmarks.py
   ```

---

## 🛡 Security & Privacy Features

### 1. SQL Guardian
Every query is intercepted by a validation layer that blocks destructive commands:
- **Blocked**: `DROP`, `DELETE`, `TRUNCATE`, `UPDATE`, `ALTER`.
- **Allowed**: `SELECT` and analytical functions only.

### 2. PII Masking
The system automatically redacts sensitive patient data before it is returned to the user or the LLM. 
- The `NAME` column in any result set is replaced with `REDACTED_PATIENT_PII`.

### 3. Role-Based Access
It is recommended to use a Snowflake user with **Read-Only (SELECT)** privileges for this application.

---

## 🛠 Tool Reference
- **SQL_TOOL**: Converts English to Snowflake SQL. Joins `Patients`, `Admissions`, and `Vitals` tables automatically.
- **DRUG_TOOL**: Provides interaction warnings and monitoring requirements for medications.
- **FILE_TOOL**: Reads clinical PDFs/Text files to provide treatment guidelines.

---

*Built by the Lead AI & Data Engineering Team.*
