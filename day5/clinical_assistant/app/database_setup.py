import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse=os.environ.get('SNOWFLAKE_WH'),
        database=os.environ.get('SNOWFLAKE_DB'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA')
    )

def setup_schema():
    print("--- Initializing Clinical Schema in Snowflake ---")
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create Tables
        cursor.execute("CREATE OR REPLACE TABLE patients (patient_id INT, name STRING, age INT, gender STRING, diagnosis STRING);")
        cursor.execute("CREATE OR REPLACE TABLE admissions (admission_id INT, patient_id INT, admission_date DATE, discharge_date DATE, department STRING);")
        cursor.execute("CREATE OR REPLACE TABLE vitals (patient_id INT, bp INT, heart_rate INT, recorded_at TIMESTAMP);")
        
        print("✅ Tables created successfully.")
    except Exception as e:
        print(f"❌ Error during schema setup: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    setup_schema()
