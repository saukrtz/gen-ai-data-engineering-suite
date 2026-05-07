import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools.knowledge_rag import setup_rag, retrieve_knowledge
from tools.snowflake_mcp import run_snowflake_query
from tools.weather_tool import get_weather

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
retriever = setup_rag()

# Schema for SQL Whitelisting
DB_DB = os.environ.get('SNOWFLAKE_DB', 'DAY5_GEN')
DB_SCHEMA_NAME = os.environ.get('SNOWFLAKE_SCHEMA', 'F1ST')

def generate_sql(user_query: str) -> str:
    """Uses Groq to translate natural language into Snowflake SQL with whitelisted columns."""
    system_prompt = f"""
    You are a Snowflake SQL expert.
    
    WHITELISTED COLUMNS: id, name, age, gender, diagnosis, bp, visit_date.
    TABLE: {DB_DB}.{DB_SCHEMA_NAME}.PATIENT_DATA
    
    RULES:
    1. Generate ONLY a valid SELECT query. No markdown.
    2. Any column in the SELECT list that is not part of an aggregate function MUST be included in the GROUP BY clause.
    3. Use fully qualified table names.
    
    EXAMPLES:
    - User: How many patients have hypertension?
      SQL: SELECT COUNT(*) FROM {DB_DB}.{DB_SCHEMA_NAME}.PATIENT_DATA WHERE diagnosis = 'Hypertension'
    - User: What is the average bp?
      SQL: SELECT AVG(bp) FROM {DB_DB}.{DB_SCHEMA_NAME}.PATIENT_DATA
    """
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}],
        temperature=0
    )
    sql = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "")
    print(f"   Generated SQL: {sql}")
    return sql

def get_routing_decision(user_query: str):
    """Uses the LLM to decide which tools are needed."""
    system_prompt = """
    Analyze the user query and decide which tools are needed. 
    
    GUIDELINES:
    - If the user mentions 'Patient', 'ID', 'Name', 'Records', or specific clinical data (BP, Age), set 'use_snowflake' to true.
    - If the user mentions 'Weather', 'Temperature', 'Climate', or 'Outside', set 'use_weather' to true.
    - If the user asks for guidelines, treatment, or advice, set 'use_rag' to true.
    
    Return a JSON object with:
    { "use_weather": bool, "use_snowflake": bool, "use_rag": bool }
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_query}],
        response_format={"type": "json_object"},
        temperature=0
    )
    return json.loads(response.choices[0].message.content)

def clinical_full_agent(user_query: str):
    print(f"\n--- Analyzing Query Flow: {user_query} ---")
    
    # 1. Smart Routing
    decision = get_routing_decision(user_query)
    print(f"   Tools Selected: {decision}")
    
    # 2. Parallel Execution based on decision
    weather_data = get_weather() if decision.get("use_weather") else None
    
    rag_context = retrieve_knowledge(user_query, retriever) if decision.get("use_rag") else ""
    
    db_data = None
    if decision.get("use_snowflake"):
        print("-> Accessing Snowflake...")
        sql = generate_sql(user_query)
        db_data = run_snowflake_query(sql)

    # 2. Final synthesis
    synthesis_prompt = f"""
    You are a Senior Clinical Data Assistant. Synthesize an answer for the doctor using the following sources:
    
    1. WEATHER DATA: {json.dumps(weather_data) if weather_data else "No weather data requested."}
    2. PATIENT DATABASE DATA: {json.dumps(db_data) if db_data else "No database data requested."}
    3. CLINICAL GUIDELINES: {rag_context}
    
    Doctor's Query: {user_query}
    
    Final Response (Professional & Grounded):
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": synthesis_prompt}]
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🏥 CLINICAL INTELLIGENCE COMMAND CENTER 🏥")
    print("="*50)
    print("Ask me anything about weather, patient data, or guidelines.")
    print("(Type 'quit' to exit)\n")

    while True:
        user_input = input("🩺 Doctor, enter your query: ")
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("\nShutting down Command Center. Goodbye!")
            break
            
        if not user_input.strip():
            continue

        try:
            result = clinical_full_agent(user_input)
            print("\n" + "-"*30)
            print("💡 ASSISTANT RESPONSE:")
            print(result)
            print("-"*30 + "\n")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
