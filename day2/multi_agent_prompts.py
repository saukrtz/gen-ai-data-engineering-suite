# multi_agent_prompts.py — three specialist prompt templates: SQL Generator, Data Validator, Schema Explainer
from groq import Groq
import os
import json

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Shared schema used across all three agents ────────────────────
schema = """
Table: orders      → columns: order_id, customer_id, product_id, amount (revenue), order_date (DATE)
Table: customers   → columns: customer_id, name, region (North/South/East/West)
Table: products    → columns: product_id, product_name, category (Electronics/Furniture)
"""

# ═══════════════════════════════════════════════════════════════════
# PROMPT TEMPLATES
# Each template has: Name, Input, Output, Constraints
# ═══════════════════════════════════════════════════════════════════

# ── 1. SQL Generator ──────────────────────────────────────────────
#   Input      : Natural language query
#   Output     : SQL + explanation in JSON
#   Constraints: Snowflake syntax
SQL_GENERATOR_TEMPLATE = {
    "name"   : "SQL Generator",
    "system" : (
        "You are an expert Snowflake SQL developer. "
        "Always use Snowflake-compatible syntax (e.g. DATEADD, CURRENT_DATE, QUALIFY, FLATTEN). "
        "Respond ONLY with a valid JSON object — no markdown, no code fences."
    ),
    "prompt" : """Act as a Data Engineer specialising in Snowflake.

Schema:
{schema}

Task (Natural Language): {input}

Constraints:
- Use Snowflake SQL syntax only
- Use DATEADD(day, -30, CURRENT_DATE) for date filtering
- Use QUALIFY for window function filtering where appropriate

Output strictly as JSON:
{{
  "name"        : "SQL Generator",
  "sql_query"   : "<Snowflake SQL query>",
  "explanation" : "<plain English explanation>",
  "syntax_note" : "<one Snowflake-specific feature used>"
}}"""
}

# ── 2. Data Validator ─────────────────────────────────────────────
#   Input      : Table name to validate
#   Output     : Validation rules + SQL checks in JSON
#   Constraints: Flag nulls, duplicates, and out-of-range values
DATA_VALIDATOR_TEMPLATE = {
    "name"   : "Data Validator",
    "system" : (
        "You are a data quality engineer. "
        "Generate validation rules and SQL checks for given tables. "
        "Respond ONLY with a valid JSON object — no markdown, no code fences."
    ),
    "prompt" : """Act as a Data Quality Engineer.

Schema:
{schema}

Task: {input}

Generate data validation rules and SQL checks for the specified table.

Output strictly as JSON:
{{
  "name"             : "Data Validator",
  "table"            : "<table being validated>",
  "validation_rules" : [
    {{
      "rule"        : "<rule name>",
      "description" : "<what it checks>",
      "sql_check"   : "<SQL query that returns violations>"
    }}
  ],
  "summary" : "<overall data quality assessment>"
}}"""
}

# ── 3. Schema Explainer ───────────────────────────────────────────
#   Input      : Schema or table name
#   Output     : Business-friendly explanation in JSON
#   Constraints: No technical jargon — explain for non-technical users
SCHEMA_EXPLAINER_TEMPLATE = {
    "name"   : "Schema Explainer",
    "system" : (
        "You are a business analyst who translates technical database schemas "
        "into simple, non-technical language that business users can understand. "
        "Respond ONLY with a valid JSON object — no markdown, no code fences."
    ),
    "prompt" : """Act as a Business Analyst.

Schema:
{schema}

Task: {input}

Explain the schema in plain language that a non-technical business user can understand.

Output strictly as JSON:
{{
  "name"   : "Schema Explainer",
  "tables" : [
    {{
      "table_name"         : "<table name>",
      "business_purpose"   : "<what this table represents in business terms>",
      "key_columns"        : "<most important columns and what they mean>",
      "relationships"      : "<how it connects to other tables in plain English>"
    }}
  ],
  "summary" : "<one paragraph overview of what this database tracks>"
}}"""
}

# ═══════════════════════════════════════════════════════════════════
# AGENT RUNNER — runs any template with any input
# ═══════════════════════════════════════════════════════════════════
def run_agent(template: dict, user_input: str) -> dict:
    """Fill the template, call Llama, parse and return the JSON result."""
    filled_prompt = template["prompt"].format(schema=schema, input=user_input)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=600,
        messages=[
            {"role": "system", "content": template["system"]},
            {"role": "user",   "content": filled_prompt}
        ]
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw), response.usage.total_tokens
    except json.JSONDecodeError:
        return {"error": "Invalid JSON returned", "raw": raw}, response.usage.total_tokens


# ═══════════════════════════════════════════════════════════════════
# MAIN — run all three agents
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":

    agents = [
        # (template,                  user_input)
        (SQL_GENERATOR_TEMPLATE,    "Find top 5 products by revenue in last 30 days"),
        (DATA_VALIDATOR_TEMPLATE,   "Validate the orders table for data quality issues"),
        (SCHEMA_EXPLAINER_TEMPLATE, "Explain the entire schema for a business audience"),
    ]

    all_results = {}

    for template, user_input in agents:
        print("=" * 60)
        print(f"  🤖 Agent : {template['name']}")
        print(f"  📝 Input : {user_input}")
        print("=" * 60)

        result, tokens = run_agent(template, user_input)

        if "error" in result:
            print(f"  ❌ {result['error']}\n  Raw: {result.get('raw','')[:200]}")
        else:
            print(json.dumps(result, indent=2))
            print(f"\n  ✅ Tokens used: {tokens}")

        all_results[template["name"]] = result
        print()

    # Save all outputs in one JSON file
    output_path = os.path.join(os.path.dirname(__file__), "multi_agent_output.json")
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"💾 All outputs saved to: multi_agent_output.json")
