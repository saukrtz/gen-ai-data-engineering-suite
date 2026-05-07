import os
import requests
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
SERVER_URL = "http://localhost:8000"

def get_tool_routing(user_query: str):
    """
    Asks the LLM to decide which tool to use.
    """
    system_prompt = """
    You are the 'Lead Clinical Data Assistant'.
    
    CRITICAL TOOL RULES:
    1. SQL_TOOL: The argument MUST be a valid Snowflake SQL query. Use for database questions.
    2. DRUG_TOOL: The argument MUST be a SINGLE DRUG NAME only (e.g., 'Aspirin'). NO SQL HERE.
    3. FILE_TOOL: The argument MUST be a filename (e.g., 'guidelines.txt').
    
    Database Schema:
    - PATIENTS (patient_id, name, age, gender, diagnosis)
    - ADMISSIONS (admission_id, patient_id, admission_date, discharge_date, department)
    - VITALS (patient_id, bp, heart_rate, recorded_at)

    Output format: ONLY JSON.
    Example: {"tool": "DRUG_TOOL", "argument": "Lisinopril"}
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def execute_tool_call(routing_decision):
    """
    Routes the decision to the actual FastAPI server endpoints.
    """
    tool = routing_decision['tool']
    arg = routing_decision['argument']
    
    if tool == "SQL_TOOL":
        resp = requests.post(f"{SERVER_URL}/run_sql", json={"query": arg})
    elif tool == "DRUG_TOOL":
        resp = requests.get(f"{SERVER_URL}/drug_check", params={"drug_name": arg})
    elif tool == "FILE_TOOL":
        resp = requests.get(f"{SERVER_URL}/read_report", params={"filename": arg})
    else:
        return "Error: Unknown tool."
    
    if resp.status_code != 200:
        return {"error": f"Server returned {resp.status_code} for {tool}. Detail: {resp.text}"}
        
    return resp.json()

def clinical_assistant_chat(user_query: str):
    """
    The end-to-end flow for the doctor.
    """
    # 1. Decide Tool
    decision = get_tool_routing(user_query)
    print(f"Agent Action: Calling {decision['tool']} with argument: {decision['argument']}")
    
    # 2. Execute Tool
    tool_results = execute_tool_call(decision)
    print(f"Raw Tool Result: {json.dumps(tool_results)}")
    
    # 3. Final Synthesized Answer
    final_prompt = f"""
    The user asked: {user_query}
    The tool returned the following data: {json.dumps(tool_results)}
    
    As a Lead Clinical Assistant, summarize this information for the doctor in a professional, concise manner.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": final_prompt}]
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    # Test queries
    print("Test 1: SQL Data")
    print(clinical_assistant_chat("How many patients are in the Cardiology department?"))
    
    print("\nTest 2: Drug Check")
    print(clinical_assistant_chat("Is it safe to take Warfarin?"))
