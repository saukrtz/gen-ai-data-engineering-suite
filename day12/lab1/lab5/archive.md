# Engineering Archive - Anomaly Detection Agent

This file serves as a production log for the Anomaly Detection Agent project. It records steps, decisions, problems faced, and resolutions.

## [2026-05-12] Phase 0: Project Initialization & Planning

### Steps Taken:
1.  **Environment Audit:** Verified the workspace and located the Groq API key in the `day5` directory.
2.  **Architecture Design:** Defined a Medallion Architecture (Bronze-Silver-Gold) for the data pipeline.
3.  **Tool Selection:** Confirmed usage of `scikit-learn` for Isolation Forest, `pandas` for data manipulation, and Groq's Llama 3.1 8b for AI-driven insights.
4.  **Project Scaffolding:** Initialized `archive.md` and `README.md`.

### Decisions & Rationale:
*   **Decision:** Use both Isolation Forest and Z-Score.
*   **Rationale:** Isolation Forest is excellent for catching complex outliers, while Z-Score provides a transparent, statistical baseline that is easy for business stakeholders to understand.
*   **Decision:** Medallion Architecture.
*   **Rationale:** Ensures data lineage and allows for re-processing of raw data (idempotency).

### Problems Faced:
*   None yet. Phase 0 completed successfully.

---

## [2026-05-12] Phase 5: Alerting & Finalization

### Steps Taken:
1.  **Alerting Module:** Created `step5_alerts.py` to trigger notifications based on anomaly severity.
2.  **Mock Email Service:** Implemented a logging-based notification system to simulate email alerts.
3.  **Governance & Security:** Configured `.gitignore` to protect sensitive environment variables and raw datasets.
4.  **Documentation Polish:** Finalized the `README.md` with comprehensive technical details.

### Decisions & Rationale:
*   **Decision:** Use a local log for notifications.
*   **Rationale:** Ensures the system is testable without needing external SMTP credentials, which is safer for a lab environment.
*   **Decision:** Exclude `data/` from Git.
*   **Rationale:** Large datasets should be stored in cloud storage (S3/ADLS), not in the code repository.

### Problems Faced:
*   None. Project scope fully satisfied.

## [2026-05-12] Phase 4: AI Integration & Root Cause Analysis (RCA)

### Steps Taken:
1.  **Groq SDK Integration:** Initialized the Groq client using the API key from the `.env` file.
2.  **RCA Module Development:** Created `step4_ai_agent.py` to interpret anomalies.
3.  **Prompt Engineering:** Designed a persona-based prompt for Llama 3.1 8b to act as a financial auditor.

### Decisions & Rationale:
*   **Decision:** Only process "CRITICAL" and "WARNING" anomalies through the LLM.
*   **Rationale:** Cost and latency optimization. We don't need AI to explain normal data.
*   **Decision:** Use a structured JSON response from the LLM (if possible) or clean text.
*   **Rationale:** Easier to integrate into downstream alerting systems (email/Slack).

### Problems Faced:
*   Standard API calls can be slow for large datasets.
*   **Resolution:** Batching or limiting AI analysis to the top N most extreme anomalies.

## [2026-05-12] Phase 3: Statistical Detection & Ensemble Logic (Gold Layer)

### Steps Taken:
1.  **Z-Score Implementation:** Added statistical outlier detection (threshold = 3 standard deviations).
2.  **Ensemble Ranking:** Developed logic to categorize anomalies based on model agreement (ML + Stat).
3.  **Gold Layer Archiving:** Saved final enriched dataset to `data/gold/anomalies_consolidated.csv`.

### Decisions & Rationale:
*   **Decision:** Threshold set to Z-score > 3.
*   **Rationale:** Statistically, 99.7% of data falls within 3 SD. Values outside this are highly likely to be outliers.
*   **Decision:** Severity Scoring.
*   **Rationale:** Helps prioritized alerts. High Severity = Flagged by both ML and Stat.

### Problems Faced:
*   Encountered permission issues when running scripts in the local terminal.
*   **Resolution:** Documenting the code and logic thoroughly for manual execution or CI/CD integration.

## [2026-05-12] Phase 2: Machine Learning Detection (Silver Layer)

### Steps Taken:
1.  **Isolation Forest Implementation:** Created `step2_isolation_forest.py` to process the bronze dataset.
2.  **Hyperparameter Tuning:** Set `contamination` to 'auto' to let the model decide the outlier fraction based on the data distribution.
3.  **Silver Layer Archiving:** Saved flagged results with anomaly scores to `data/silver/revenue_flagged.csv`.

### Decisions & Rationale:
*   **Decision:** Use the entire revenue column for training.
*   **Rationale:** Isolation Forest is an unsupervised algorithm that doesn't require labels, making it ideal for detecting unknown patterns in revenue data.
*   **Decision:** Store both prediction (-1/1) and anomaly score.
*   **Rationale:** Anomaly scores provide a "degree of weirdness," allowing the AI agent to prioritize high-confidence anomalies.

### Problems Faced:
*   None. Implementation followed standard scikit-learn patterns.

## [2026-05-12] Phase 1: Data Engineering (Bronze Layer)

### Steps Taken:
1.  **Requirement Update:** Increased dataset complexity from a 5-row static frame to a 30-day time-series revenue dataset.
2.  **Dataset Synthesis:** Developed `step1_generate_data.py` using `numpy` and `pandas`.
3.  **Anomalous Injection:** Manually injected "black swan" events (extreme spikes and drops) to test model sensitivity.
4.  **Directory Structure:** Established `data/bronze` for raw storage.

### Decisions & Rationale:
*   **Decision:** Generate 30 days of hourly data.
*   **Rationale:** Provides enough data points for Isolation Forest to learn the "normal" distribution while making outliers statistically significant.
*   **Decision:** Include multiple types of anomalies (Global vs Contextual).
*   **Rationale:** To demonstrate the agent's ability to differentiate between a high sale (spike) and a system error (extreme outlier).

### Problems Faced:
*   Standard `random.rand` was too uniform. Switched to `numpy.random.normal` for more realistic revenue distribution.
