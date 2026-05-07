import os
import requests
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from tools.knowledge_rag import setup_rag, retrieve_guidelines

load_dotenv()

# Step 4 & 5: LLM Agent Orchestration & Response Synthesis
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
retriever = setup_rag()
MCP_URL = "http://localhost:8000/execute_sql"

DB_SCHEMA = """
Table: patient_data
Columns: id (INT), name (TEXT), age (INT), gender (TEXT), bp (INT), diagnosis (TEXT), visit_date (DATE)
"""

def generate_sql(query: str) -> str:
    """Uses LLM to translate natural language to SQL based on schema."""
    prompt = PromptTemplate.from_template(
        "You are an expert SQL data analyst. Generate ONLY a valid SQLite query for the following request. "
        "Do not include markdown formatting, explanations, or quotes.\n"
        "Schema: {schema}\n"
        "Request: {request}\n"
        "SQL Query:"
    )
    # Corrected invocation for LangChain
    chain = prompt | llm
    sql_query = chain.invoke({"schema": DB_SCHEMA, "request": query}).content.strip()
    return sql_query.replace("```sql", "").replace("```", "").strip()

def execute_mcp_query(sql_query: str) -> str:
    """Sends the SQL to the FastAPI MCP server."""
    try:
        response = requests.post(MCP_URL, json={"query": sql_query})
        if response.status_code == 200:
            res_json = response.json()
            if res_json["status"] == "success":
                return json.dumps(res_json["data"])
            return f"Database Error: {res_json['detail']}"
        return f"HTTP Error: {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

def clinical_assistant(user_query: str) -> str:
    """Main routing and synthesis function."""
    print("\n--- Processing Clinical Query ---")
    
    # 1. Intent Detection (Heuristic based on case study)
    needs_guidance = any(word in user_query.lower() for word in ["treatment", "guideline", "diagnose", "bp is"])
    needs_data = any(word in user_query.lower() for word in ["how many", "count", "patients", "average", "show"])
    
    rag_context = ""
    db_context = ""
    
    # 2. Parallel Execution
    if needs_guidance:
        print("-> Retrieving Medical Guidelines (RAG)...")
        rag_context = retrieve_guidelines(user_query, retriever)
        
    if needs_data:
        print("-> Querying Clinical Database (MCP)...")
        sql = generate_sql(user_query)
        print(f"   Generated SQL: {sql}")
        db_context = execute_mcp_query(sql)

    # 3. Final Synthesis
    synthesis_prompt = PromptTemplate.from_template(
        "You are an AI Clinical Decision Assistant. Answer the doctor's query based ONLY on the provided context.\n"
        "If the context does not contain the answer, state that you do not have enough information.\n\n"
        "User Query: {query}\n\n"
        "Medical Guidelines Context:\n{rag_context}\n\n"
        "Patient Database Context:\n{db_context}\n\n"
        "Final Professional Response:"
    )
    
    chain = synthesis_prompt | llm
    final_response = chain.invoke({
        "query": user_query, 
        "rag_context": rag_context if rag_context else "None required.",
        "db_context": db_context if db_context else "None required."
    })
    
    return final_response.content

if __name__ == "__main__":
    test_query = "Patient BP is 150. What is the treatment and how many similar cases are there?"
    result = clinical_assistant(test_query)
    print("\n=== Final Clinical Output ===")
    print(result)
