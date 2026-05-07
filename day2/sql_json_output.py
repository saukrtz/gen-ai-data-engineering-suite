# sql_json_output.py — generates SQL + explanation in machine-readable JSON format
from groq import Groq
import os
import json

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Database schema ───────────────────────────────────────────────
schema = """
Table: orders      → columns: order_id, customer_id, product_id, amount (revenue), order_date
Table: customers   → columns: customer_id, name, region
Table: products    → columns: product_id, product_name, category
"""

# ── Natural language query ────────────────────────────────────────
natural_language_query = "Find top 5 products by revenue in last 30 days"

# ── Prompt — instructs Llama to return ONLY valid JSON ────────────
prompt = f"""
You are a SQL generator. Given the database schema and a natural language query, 
generate a response in strict JSON format.

Database Schema:
{schema}

Natural Language Query:
"{natural_language_query}"

Return your response ONLY as a valid JSON object with exactly these two fields:
{{
  "query": "<the complete SQL query as a single string>",
  "explanation": "<a plain English explanation of what the SQL does>"
}}

Do not include anything outside the JSON object. No markdown, no code fences, no extra text.
"""

print("=" * 60)
print("  📦 SQL JSON Generator — Machine-Readable Output")
print("=" * 60)
print(f"\n📝 Query : {natural_language_query}\n")

# ── Send to Groq / Llama ──────────────────────────────────────────
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    max_tokens=500,
    messages=[
        {
            "role": "system",
            "content": (
                "You are an expert SQL developer. "
                "You always respond with valid, parseable JSON only. "
                "Never include markdown, code fences, or any text outside the JSON object."
            )
        },
        {"role": "user", "content": prompt}
    ]
)

raw_output = response.choices[0].message.content.strip()

# ── Parse and validate the JSON response ─────────────────────────
print("🤖 Raw Response from Llama:")
print("─" * 60)
print(raw_output)
print("─" * 60)

try:
    # Parse the JSON — will raise an error if Llama didn't return valid JSON
    result = json.loads(raw_output)

    print("\n✅ Valid JSON received!\n")
    print(f"📄 SQL Query:\n{result['query']}\n")
    print(f"💬 Explanation:\n{result['explanation']}")

    # Save the structured output to a JSON file
    output_path = os.path.join(os.path.dirname(__file__), "generated_sql_output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n💾 Saved to: generated_sql_output.json")

except json.JSONDecodeError as e:
    # If Llama returned something that isn't valid JSON
    print(f"\n❌ JSON parsing failed: {e}")
    print("Tip: Llama occasionally wraps output in markdown. Raw output saved for inspection.")

print(f"\n✅ Tokens used : {response.usage.total_tokens}")
print("=" * 60)
