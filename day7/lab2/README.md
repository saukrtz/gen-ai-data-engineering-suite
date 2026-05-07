# AI-Powered Healthcare Pipeline (Medallion Architecture)

## Overview
This project implements a production-grade healthcare data pipeline using PySpark, Delta Lake, and Prefect. It follows the Medallion Architecture to process patient data from raw ingestion to business insights.

### Architecture Layers
- **Bronze (Raw)**: Ingests CSV data into Delta format with partitioning by `visit_date`. Supports incremental ingestion.
- **Silver (Cleaned)**: Standardizes data, fills null billing amounts, and removes duplicates.
- **Gold (Aggregated)**: Performs business aggregations (billing by diagnosis) using idempotent MERGE operations.

## Project Structure
```text
pipeline/
 ├── bronze/        # Raw Ingestion Logic (ingest.py)
 ├── silver/        # Data Cleaning Logic (process.py)
 ├── gold/          # Aggregation & MERGE Logic (aggregate.py)
 ├── dags/          # Prefect Flow Orchestration (healthcare_flow.py)
 ├── tests/         # Pytest Suite (test_pipeline.py)
 ├── utils/         # Groq LLM Helper (llm_helper.py)
 └── main.py        # Entry Point
```

## Setup
1. **Install Dependencies**:
   ```bash
   pip install pyspark prefect delta-spark pytest requests
   ```
2. **Environment**:
   Ensure your `GROQ_API_KEY` is set to utilize the AI-powered development features.

## Usage
### Running the Pipeline
```bash
python3 pipeline/dags/healthcare_flow.py
```
### Running Tests
```bash
pytest pipeline/tests/
```
