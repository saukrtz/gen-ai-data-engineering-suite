import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MCP_SERVER_URL = "http://localhost:8001"

def fetch_dynamic_schema():
    """Asks the MCP server for the current database schema."""
    print("[1/3] Fetching dynamic schema from Snowflake...")
    try:
        response = requests.get(f"{MCP_SERVER_URL}/get_schema")
        response.raise_for_status()
        return response.json().get("schema", {})
    except Exception as e:
        print(f"Error fetching schema: {e}")
        return {}

def format_schema_for_llm(schema_dict):
    """Converts the schema dictionary into a readable string for the LLM prompt."""
    schema_str = ""
    for table, columns in schema_dict.items():
        schema_str += f"\nTable: {table}\nColumns:\n"
        for col in columns:
            schema_str += f"  - {col['name']} ({col['type']})\n"
    return schema_str

def get_sql_from_llm(user_prompt, schema_context):
    """Generates SQL using the dynamic schema context."""
    system_prompt = f"""
    You are an expert SQL assistant for Snowflake.
    Here is the DYNAMIC schema of the database:
    {schema_context}
    
    Instructions:
    - Only output the SQL query itself.
    - Do not include any explanation or markdown formatting.
    - Use the provided tables and columns.
    """
    
    print("[2/3] Generating SQL via Groq (with dynamic context)...")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )
    return completion.choices[0].message.content.strip()

def main():
    print("--- Dynamic AI Data Agent ---")
    
    # 1. Get Schema automatically
    schema_dict = fetch_dynamic_schema()
    if not schema_dict:
        print("Could not retrieve schema. Is the server running on port 8001?")
        return
    
    schema_context = format_schema_for_llm(schema_dict)
    
    # 2. Get User Question
    user_query = input("\nAsk anything about your data: ")
    
    # 3. Generate SQL
    sql = get_sql_from_llm(user_query, schema_context)
    print(f"Generated SQL: {sql}")
    
    # 4. Execute
    print("[3/3] Executing on Snowflake...")
    try:
        response = requests.post(f"{MCP_SERVER_URL}/run_sql", json={"query": sql})
        result = response.json()
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("\n✅ Results:")
            print(result["result"])
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    main()
