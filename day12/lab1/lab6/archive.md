# Engineering Archive - Configurable Threshold Monitoring

## [2026-05-12] Phase 0: Project Initialization & Planning

### Steps Taken:
1.  **Requirement Audit:** Analyzed the objectives for Lab 6 (Configurable Thresholds).
2.  **Architecture Design:** Proposed a Metadata-Driven Monitoring Framework (Config-as-Code).
3.  **Tool Selection:** YAML for configuration, Pandas for calculation, Groq Llama 3.1 8b for AI alerting.

### Decisions & Rationale:
*   **Decision:** Use YAML for threshold definitions.
*   **Rationale:** Allows for dynamic updates without code changes, improving maintainability.

### Problems Faced:
*   None yet.

---

## [2026-05-12] Phase 1: Configuration & Monitoring Engine

### Steps Taken:
1.  **Metadata Design:** Created `config/thresholds.yaml` to centralize DQ rules (Null Rate limits, Severity).
2.  **Dataset Synthesis:** Developed `step1_generate_data.py` to produce realistic revenue data with specific null patterns to trigger alerts.
3.  **Engine Logic:** Implemented `step2_monitor_engine.py` using a generic `MonitoringEngine` class that calculates null rates dynamically for any column specified in the config.

### Decisions & Rationale:
*   **Decision:** Move thresholds to YAML.
*   **Rationale:** Decouples monitoring logic from business rules, allowing for "Hot Swapping" thresholds without code deployments.
*   **Decision:** Separate Data Generation from Engine logic.
*   **Rationale:** Follows the modular "Bronze/Silver/Gold" pattern established in previous labs.

---

## [2026-05-12] Phase 2: AI-Powered Alerting & Notifications

### Steps Taken:
1.  **AI Integration:** Developed `step3_ai_alerts.py` to process DQ failures via Groq's Llama 3.1 8b.
2.  **Severity Orchestration:** Engineered a prompt that asks the AI to evaluate the "Downstream Impact" of specific null rates.
3.  **Notification Mocking:** Built a Slack notification service that outputs structured JSON to `slack_alerts.log`.

### Decisions & Rationale:
*   **Decision:** Use AI for "Impact Analysis" rather than just static severity.
*   **Rationale:** A 5% null rate in revenue is more critical for a Finance team than a 5% null rate in "Region" for a Marketing team. AI can contextualize these differences.

---

## [2026-05-12] Phase 3: Repository Readiness & Cleanup

### Steps Taken:
1.  **Environment Isolation:** Created a root `.gitignore` in `lab1/` to exclude data files, logs, and python artifacts.
2.  **Validation:** Verified the end-to-end flow: Generate Data -> Monitor -> AI Analysis -> Slack Alert.
3.  **Final Documentation:** Updated `README.md` and `archive.md` with final architecture and decision logs.

### Decisions & Rationale:
*   **Decision:** Add `.gitignore` at the `lab1` level.
*   **Rationale:** Simplifies repository management for the user who is managing multiple labs simultaneously.

### Problems Faced:
*   Initial attempt to commit failed due to missing pathspec for `.gitignore`.
*   **Resolution:** Created the missing `.gitignore` file and staged all labs properly.
