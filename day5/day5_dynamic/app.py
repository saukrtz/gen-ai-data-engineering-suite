from fastapi import FastAPI
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

def get_db_connection():
    return snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse=os.environ.get('SNOWFLAKE_WH'),
        database=os.environ.get('SNOWFLAKE_DB'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA')
    )

@app.get("/get_schema")
def get_schema():
    """Fetches all table names and their columns dynamically from Snowflake."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Get all tables
        cursor.execute("SHOW TABLES")
        tables = [row[1] for row in cursor.fetchall()]
        
        schema_info = {}
        
        # 2. Get columns for each table
        for table in tables:
            cursor.execute(f"DESCRIBE TABLE {table}")
            columns = [{"name": row[0], "type": row[1]} for row in cursor.fetchall()]
            schema_info[table] = columns
            
        cursor.close()
        conn.close()
        return {"schema": schema_info}
    except Exception as e:
        return {"error": str(e)}

@app.post("/run_sql")
def run_sql(payload: dict):
    query = payload.get("query")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cursor.close()
        conn.close()
        return {"query": query, "result": [dict(zip(columns, row)) for row in result]}
    except Exception as e:
        return {"query": query, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Running on 8001 to avoid conflict
