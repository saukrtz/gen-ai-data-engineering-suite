import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Load credentials
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MCP_SERVER_URL = "http://localhost:8000/run_sql"

def get_sql_from_llm(user_prompt):
    """
    Uses Groq to convert natural language into a Snowflake SQL query.
    """
    system_prompt = """
    You are an expert SQL assistant for Snowflake. 
    The database has the following schema:
    
    Table: SALES_DATA
    Columns:
    - ID (NUMBER)
    - REGION (VARCHAR)
    - REVENUE (FLOAT)
    - SALE_DATE (DATE)

    Instructions:
    - Only output the SQL query itself.
    - Do not include any explanation or markdown formatting.
    - Use the provided table and columns.
    """
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )
    
    sql_query = completion.choices[0].message.content.strip()
    return sql_query

def call_mcp_server(sql_query):
    """
    Sends the generated SQL query to the FastAPI MCP server.
    """
    payload = {"query": sql_query}
    try:
        response = requests.post(MCP_SERVER_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("--- Natural Language to Snowflake Agent ---")
    user_query = input("\nAsk a question (e.g., 'Show top 5 customers'): ")
    
    print("\n[1/2] Converting to SQL using Groq...")
    sql = get_sql_from_llm(user_query)
    print(f"Generated SQL: {sql}")
    
    print("\n[2/2] Executing on Snowflake via MCP Server...")
    result = call_mcp_server(sql)
    
    if "error" in result:
        print(f"\n❌ Execution failed: {result['error']}")
    else:
        print("\n✅ Results:")
        print(result["result"])

if __name__ == "__main__":
    main()
