# 🏆 Agentic Retail Analytics: Final Project Archive (Day 6)

This archive documents the transition from manual dbt modeling to an AI-powered "Architect" approach for Retail Analytics.

---

## 1. Project Mission
**Objective**: Build a robust Retail Analytics System in Snowflake using dbt, progressing from manual SQL modeling to an automated Agentic Pipeline using Groq's Llama 3.1.

---

## 2. Iteration 1: Manual Star Schema
- **Folder**: `gen_ai/day6/retail_project/`
- **Models**: `stg_orders`, `stg_customers`, `stg_products`, `dim_customer`, `dim_product`, `fact_sales`.
- **Outcome**: Successfully established the foundation of a star schema.

---

## 3. Iteration 2: Agentic v2 Pipeline
- **Folder**: `gen_ai/day6/agentic_dbt/`
- **Models**: `stg_v2_*`, `dim_v2_*`, `fact_v2_sales`.
- **AI Logic (Groq Llama 3.1)**:
    - **Calculated Columns**: Automatically added `tax_amount` and `total_amount_with_tax`.
    - **Clean Data**: Normalized customer names to uppercase.
    - **Business Rules**: Flagged high-priority product categories.
- **Outcome**: A smarter, faster, and more detailed analytical dataset.

---

## 4. Data Quality & Validation
All models were validated using dbt's native testing framework:
- **Total Models**: 6
- **Total Tests**: 6
- **Result**: 100% Pass Rate ✅

---

## 5. Technical Stack
- **Database**: Snowflake (DAY6_GEN)
- **Transform**: dbt Core (1.11.8)
- **AI Brain**: Groq Llama 3.1 (via Architect.py)
- **Environment**: dbt-env (Local Virtual Environment)

---
*Archive Compiled by Antigravity AI Agent.*
