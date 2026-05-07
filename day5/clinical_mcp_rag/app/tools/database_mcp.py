import sqlite3
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

# Step 3: Structured Data Querying (MCP Server Setup)
app = FastAPI(title="Clinical MCP Server")

DB_PATH = os.path.join(os.path.dirname(__file__), "../../hospital.db")

def setup_database():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_data (
            id INT,
            name TEXT,
            age INT,
            gender TEXT,
            bp INT,
            diagnosis TEXT,
            visit_date DATE
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM patient_data")
    if cursor.fetchone()[0] == 0:
        data = [
            (1, "John Doe", 45, "M", 150, "Hypertension", "2024-05-01"),
            (2, "Jane Smith", 52, "F", 130, "Normal", "2024-05-02"),
            (3, "Ravi Kumar", 60, "M", 160, "Hypertension", "2024-05-03"),
            (4, "Anita Sharma", 38, "F", 120, "Normal", "2024-05-04"),
            (5, "Rahul Verma", 55, "M", 170, "Hypertension", "2024-05-05")
        ]
        cursor.executemany("INSERT INTO patient_data VALUES (?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
    return conn

conn = setup_database()

class SQLQuery(BaseModel):
    query: str

@app.post("/execute_sql")
def execute_sql(payload: SQLQuery):
    try:
        # Use pandas for easy JSON serialization
        df = pd.read_sql_query(payload.query, conn)
        return {"status": "success", "data": df.to_dict(orient="records")}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
