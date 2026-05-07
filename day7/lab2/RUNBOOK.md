# AI-Powered Healthcare Pipeline RUNBOOK

## Execution Steps
1. **Full Pipeline Run**:
   Run the Prefect flow to execute Bronze -> Silver -> Gold.
   ```bash
   python3 pipeline/dags/healthcare_flow.py
   ```
2. **Manual Layer Execution**:
   Each layer can be run independently for debugging:
   - Bronze: `python3 pipeline/bronze/ingest.py`
   - Silver: `python3 pipeline/silver/process.py`
   - Gold: `python3 pipeline/gold/aggregate.py`

## Failure Handling
### 1. Missing Source Files
- **Symptom**: Bronze layer fails with `FileNotFoundError`.
- **Action**: Verify `data/patients.csv` exists and is readable.

### 2. Null Values in Critical Columns
- **Symptom**: Aggregations show "Unknown" or 0 values.
- **Action**: Silver layer handles null `billing_amount` by defaulting to 0. Check source data if more critical fields are null.

### 3. Duplicate Records
- **Symptom**: Gold layer totals are higher than expected.
- **Action**: Silver layer automatically drops duplicate `patient_id` records. Verify unique constraints in the source.

## Recovery Procedures
### 1. Corrupted Delta Tables
- **Action**: Delete the specific directory in `output/` and re-run the pipeline. Delta Lake handles overwrite/re-creation safely.

### 2. Job Interruption
- **Action**: The pipeline is idempotent. You can re-run the Prefect flow, and the Gold layer `MERGE` will ensure data consistency without duplicates.
