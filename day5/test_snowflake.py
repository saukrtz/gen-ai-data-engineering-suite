import snowflake.connector
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def test_connection():
    print("Connecting to Snowflake...")
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
        cursor.execute("SELECT CURRENT_VERSION(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        row = cursor.fetchone()
        
        print("\n✅ Connection Successful!")
        print(f"Snowflake Version: {row[0]}")
        print(f"Warehouse: {row[1]}")
        print(f"Database: {row[2]}")
        print(f"Schema: {row[3]}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"\n❌ Connection Failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
