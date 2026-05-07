from fastapi import FastAPI
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = FastAPI()

def run_query(query):
    # Fetch credentials from environment variables for security
    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER', 'YOUR_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD', 'YOUR_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT', 'YOUR_ACCOUNT'),
        warehouse=os.environ.get('SNOWFLAKE_WH', 'YOUR_WH'),
        database=os.environ.get('SNOWFLAKE_DB', 'YOUR_DB'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA', 'PUBLIC')
    )

    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        # Get column names
        columns = [col[0] for col in cursor.description]
        # Return as list of dicts for better JSON response
        return [dict(zip(columns, row)) for row in result]
    finally:
        cursor.close()
        conn.close()

@app.post("/run_sql")
def run_sql(payload: dict):
    query = payload.get("query")
    if not query:
        return {"error": "No query provided"}
    try:
        result = run_query(query)
        return {"query": query, "result": result}
    except Exception as e:
        return {"query": query, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
