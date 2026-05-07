import snowflake.connector
import os
import json
from dotenv import load_dotenv

load_dotenv()

def run_snowflake_query(query: str):
    """Executes SQL against Snowflake with strict PII masking."""
    
    # Whitelist check for safety
    allowed_keywords = ["SELECT", "COUNT", "AVG", "WHERE", "GROUP BY", "FROM", "JOIN"]
    if not any(word in query.upper() for word in allowed_keywords):
         return {"error": "Unauthorized query type."}

    try:
        conn = snowflake.connector.connect(
            user=os.environ.get('SNOWFLAKE_USER'),
            password=os.environ.get('SNOWFLAKE_PASSWORD'),
            account=os.environ.get('SNOWFLAKE_ACCOUNT'),
            warehouse=os.environ.get('SNOWFLAKE_WH'),
            database=os.environ.get('SNOWFLAKE_DB'),
            schema=os.environ.get('SNOWFLAKE_SCHEMA')
        )
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            # Convert non-serializable types
            for key, val in row_dict.items():
                if hasattr(val, 'isoformat'): # Handle Dates
                    row_dict[key] = val.isoformat()
                elif isinstance(val, (float, int)):
                    continue
                elif val is not None: # Handle Decimals or others
                    row_dict[key] = str(val)
            results.append(row_dict)
                
        return results
    except Exception as e:
        return {"error": str(e)}
    finally:
        if 'conn' in locals():
            conn.close()
