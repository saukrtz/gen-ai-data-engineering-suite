from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryPayload(BaseModel):
    query: str

@app.post("/run_sql")
def run_sql(payload: QueryPayload):
    # This is a mock tool execution layer
    print(f"Executing tool with query: {payload.query}")
    return {
        "status": "success",
        "message": "Tool working",
        "query": payload.query
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
