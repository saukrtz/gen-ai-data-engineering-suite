import os
import requests
from groq import Groq
from dotenv import load_dotenv

# Load credentials
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MOCK_API_URL = "http://127.0.0.1:8002/run_sql"

def run_lab_3():
    print("--- LAB 3: Basic Tool Calling Loop ---")
    
    # 1. The Prompt Template
    user_input = "Show total revenue by region"
    system_prompt = """
    You are a SQL generator.
    Table: sales_data(id, region, revenue)
    
    Instructions:
    - Only output the SQL query.
    - No markdown formatting.
    """
    
    print(f"\n[1/3] Prompting LLM: '{user_input}'")
    
    # 2. LLM -> SQL
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1
    )
    sql_query = completion.choices[0].message.content.strip()
    print(f"Generated SQL: {sql_query}")
    
    # 3. SQL -> API Call
    print(f"\n[2/3] Sending SQL to Mock API...")
    payload = {"query": sql_query}
    try:
        response = requests.post(MOCK_API_URL, json=payload)
        response.raise_for_status()
        api_result = response.json()
        
        # 4. Outcome
        print("\n[3/3] Final Outcome from API:")
        print(api_result)
        
    except Exception as e:
        print(f"❌ API Call failed: {e}")

if __name__ == "__main__":
    run_lab_3()
