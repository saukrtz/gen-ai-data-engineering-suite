import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MCP_SERVER_URL = "http://localhost:8001"

def fetch_dynamic_schema():
    try:
        response = requests.get(f"{MCP_SERVER_URL}/get_schema")
        response.raise_for_status()
        return response.json().get("schema", {})
    except:
        return {}

def format_schema_for_llm(schema_dict):
    schema_str = ""
    for table, columns in schema_dict.items():
        schema_str += f"\nTable: {table}\nColumns:\n"
        for col in columns:
            schema_str += f"  - {col['name']} ({col['type']})\n"
    return schema_str

def process_prompt(user_input):
    """The main brain function that handles everything from input to result."""
    # 1. Fetch Schema
    schema_dict = fetch_dynamic_schema()
    schema_context = format_schema_for_llm(schema_dict)
    
    # 2. Generate SQL
    system_prompt = f"You are an expert SQL assistant for Snowflake. Schema:\n{schema_context}\nOnly output SQL. No markdown."
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.1
    )
    sql = completion.choices[0].message.content.strip()
    
    # 3. Execute
    try:
        response = requests.post(f"{MCP_SERVER_URL}/run_sql", json={"query": sql})
        result = response.json()
        return result.get("result") or result.get("error")
    except Exception as e:
        return str(e)
