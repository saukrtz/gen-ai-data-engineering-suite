# data_engineer_agent.py — uses a reusable prompt template with {schema} and {task} placeholders
from groq import Groq
import os
import json

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Schema definition (injected into the prompt template) ─────────
schema = """
Table: orders      → columns: order_id, customer_id, product_id, amount (revenue), order_date (DATE)
Table: customers   → columns: customer_id, name, region (North/South/East/West)
Table: products    → columns: product_id, product_name, category (Electronics/Furniture)
"""

# ── Task definition (injected into the prompt template) ──────────
task = "Find top 5 products by revenue in the last 30 days"

# ── Prompt template — {schema} and {task} are injected below ──────
# This is a reusable template: change schema or task without rewriting the prompt
prompt_template = """Act as a Data Engineer.

Schema: {schema}

Task: {task}

Output: JSON in exactly this format:
{{
  "sql_query"   : "<the SQL query as a single string>",
  "explanation" : "<plain English explanation of what the query does>",
  "tables_used" : ["<list of table names used in the query>"],
  "complexity"  : "<Simple | Moderate | Complex>"
}}

Return ONLY the JSON object. No markdown, no code fences, no text outside the JSON.
"""

# ── Fill in the placeholders ──────────────────────────────────────
prompt = prompt_template.format(schema=schema, task=task)

print("=" * 60)
print("  🛠️  Data Engineer Agent — Template Prompt")
print("=" * 60)
print(f"\n📋 Schema  : {schema.strip()}")
print(f"\n🎯 Task    : {task}")
print("\n🤖 Generating output...\n")

# ── Send to Groq / Llama ──────────────────────────────────────────
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    max_tokens=500,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a senior Data Engineer who generates precise SQL. "
                "Always respond with valid JSON only. "
                "No markdown, no code fences, no extra text outside the JSON object."
            )
        },
        {"role": "user", "content": prompt}
    ]
)

raw_output = response.choices[0].message.content.strip()

# ── Parse and display the JSON response ──────────────────────────
print("─" * 60)
try:
    result = json.loads(raw_output)

    print(f"✅ Valid JSON received!\n")
    print(f"📄 SQL Query:\n{result.get('sql_query', 'N/A')}\n")
    print(f"💬 Explanation:\n{result.get('explanation', 'N/A')}\n")
    print(f"📦 Tables Used : {result.get('tables_used', [])}")
    print(f"⚙️  Complexity  : {result.get('complexity', 'N/A')}")

    # Save structured JSON output
    output_path = os.path.join(os.path.dirname(__file__), "agent_output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n💾 Saved to: agent_output.json")

except json.JSONDecodeError as e:
    print(f"❌ JSON parse error: {e}")
    print(f"Raw output:\n{raw_output}")

print(f"\n✅ Tokens used : {response.usage.total_tokens}")
print("=" * 60)
