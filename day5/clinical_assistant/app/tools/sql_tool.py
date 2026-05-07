import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def validate_query(query: str):
    """Prevents destructive SQL commands."""
    forbidden = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "ALTER", "INSERT"]
    if any(cmd in query.upper() for cmd in forbidden):
        raise Exception(f"Security Alert: Destructive command '{query}' blocked.")

def mask_pii(results):
    """Redacts sensitive columns like 'NAME' to protect patient privacy."""
    for row in results:
        if "NAME" in row:
            row["NAME"] = "REDACTED_PATIENT_PII"
    return results

def run_query(query: str):
    """Executes a SQL query against the Snowflake clinical database with security checks."""
    validate_query(query)
    
    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse=os.environ.get('SNOWFLAKE_WH'),
        database=os.environ.get('SNOWFLAKE_DB'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA')
    )
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Apply PII Masking
        return mask_pii(results)
    finally:
        cursor.close()
        conn.close()
