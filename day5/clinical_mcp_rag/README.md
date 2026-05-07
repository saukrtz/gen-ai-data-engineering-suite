# AI Clinical Decision Assistant (Modular Edition) 🩺🤖

A high-precision medical agent that combines unstructured knowledge (RAG) with structured patient data (SQL) to provide grounded clinical decision support.

---

## 🌟 Key Features
- **Intelligent Routing**: Automatically detects if a query needs medical guidelines, patient statistics, or both.
- **Deterministic SQL**: Uses a whitelisted schema to prevent SQL hallucinations and errors.
- **Semantic RAG**: Powered by FAISS and local embeddings for near-instant search of clinical guidelines.
- **Grounded Responses**: All AI answers are strictly tied to the retrieved context to ensure safety.

---

## 🛠 Project Components
- `app/agent_orchestrator.py`: The main AI logic and synthesis engine.
- `app/tools/knowledge_rag.py`: The vector search pipeline for guidelines.
- `app/tools/database_mcp.py`: The SQLite database server for patient data.

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have the required libraries installed:
```bash
pip install fastapi uvicorn langchain-groq faiss-cpu langchain-huggingface sentence-transformers pandas requests python-dotenv
```

### 2. Configuration
Create a `.env` file in the project root with your Groq API Key:
```env
GROQ_API_KEY=your_key_here
```

### 3. Run the System

**Terminal 1 (Start the Database Server):**
```bash
cd app/tools
python3 database_mcp.py
```

**Terminal 2 (Run the Agent):**
```bash
cd app
python3 agent_orchestrator.py
```

---

## 📊 Sample Queries to Try
- *"How many patients are in our database?"*
- *"What is the treatment for a patient with BP 150?"*
- *"Show me similar cases for Stage 1 Hypertension."*

---
*Developed for the Clinical Data Science Team.*
