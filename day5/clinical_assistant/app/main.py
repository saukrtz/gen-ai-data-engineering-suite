from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import our tools
from tools.sql_tool import run_query
from tools.drug_tool import check_drug_safety
from tools.file_tool import read_clinical_report

load_dotenv()

app = FastAPI(title="Clinical Data Assistant MCP Server")

class SQLPayload(BaseModel):
    query: str

class DrugPayload(BaseModel):
    drug_name: str

class FilePayload(BaseModel):
    filename: str

@app.get("/")
def read_root():
    return {"message": "Clinical Data Assistant MCP Server is Running"}

@app.post("/run_sql")
def sql_endpoint(payload: SQLPayload):
    """Endpoint for clinical data queries (Snowflake)."""
    try:
        results = run_query(payload.query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drug_check")
def drug_endpoint(drug_name: str):
    """Endpoint for drug interaction and safety checks."""
    return check_drug_safety(drug_name)

@app.get("/read_report")
def report_endpoint(filename: str):
    """Endpoint to read clinical guidelines/reports."""
    return read_clinical_report(filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
