# lab6_batch_pipeline.py — LAB 6: Batch Processing (Pipeline Simulation)
# Objective: Simulate real Data Engineering workflow by processing multiple SQL tasks in a loop
from groq import Groq
import os
import json
import time

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Shared schema injected into every task prompt ─────────────────
schema = """
Table: orders      → columns: order_id, customer_id, product_id, amount (revenue), order_date (DATE)
Table: customers   → columns: customer_id, name, region (North/South/East/West)
Table: products    → columns: product_id, product_name, category (Electronics/Furniture)
"""

# ═══════════════════════════════════════════════════════════════════
# STEP 1 — Define multiple tasks (simulating a real pipeline queue)
# ═══════════════════════════════════════════════════════════════════
tasks = [
    "Top 3 customers",
    "Total revenue by region",
    "Daily sales trend"
]


# ═══════════════════════════════════════════════════════════════════
# METHOD — generate_sql_safe
# Wraps the API call with error handling so one failure
# doesn't crash the entire pipeline batch
# ═══════════════════════════════════════════════════════════════════
def generate_sql_safe(schema: str, task: str) -> dict:
    """
    Sends a natural language task to Llama and returns a structured JSON result.

    Args:
        schema (str): The database schema description.
        task   (str): A natural language task to convert to SQL.

    Returns:
        dict: {
            "task"       : original task,
            "sql_query"  : generated SQL,
            "explanation": plain English explanation,
            "status"     : "success" or "error",
            "tokens_used": token count
        }
    """
    # Build the prompt for this specific task
    prompt = f"""
Act as a Data Engineer.

Schema: {schema}

Task: {task}

Output strictly as JSON (no markdown, no extra text):
{{
  "sql_query"  : "<the SQL query as a single string>",
  "explanation": "<plain English explanation of what the SQL does>"
}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=400,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior Data Engineer. "
                        "Generate clean, standard SQL for the given task. "
                        "Respond ONLY with a valid JSON object. No markdown or code fences."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)   # Will raise if Llama returns invalid JSON

        return {
            "task"       : task,
            "sql_query"  : parsed.get("sql_query", ""),
            "explanation": parsed.get("explanation", ""),
            "status"     : "success",
            "tokens_used": response.usage.total_tokens
        }

    except json.JSONDecodeError:
        # Llama returned something that isn't valid JSON — save raw for inspection
        return {
            "task"       : task,
            "sql_query"  : "",
            "explanation": f"JSON parse error. Raw: {raw[:200]}",
            "status"     : "json_error",
            "tokens_used": 0
        }

    except Exception as e:
        # Catch API errors (rate limit, network, etc.) without crashing the pipeline
        return {
            "task"       : task,
            "sql_query"  : "",
            "explanation": str(e),
            "status"     : "api_error",
            "tokens_used": 0
        }


# ═══════════════════════════════════════════════════════════════════
# STEP 2 — Loop through all tasks (pipeline execution)
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":

    print("=" * 60)
    print("  ⚙️  LAB 6: Batch Pipeline — Processing Tasks")
    print(f"  Total tasks : {len(tasks)}")
    print("=" * 60)

    all_results = []

    for i, task in enumerate(tasks, start=1):
        print(f"\n[{i}/{len(tasks)}] Task: {task}")
        print("─" * 60)

        # Call the safe method for each task
        result = generate_sql_safe(schema, task)

        # Print the output
        if result["status"] == "success":
            print(f"✅ SQL:\n{result['sql_query']}")
            print(f"\n💬 Explanation:\n{result['explanation']}")
            print(f"\n🔢 Tokens used: {result['tokens_used']}")
        else:
            print(f"❌ Status  : {result['status']}")
            print(f"   Details : {result['explanation']}")

        all_results.append(result)

        # Small delay between calls to stay within rate limits
        if i < len(tasks):
            time.sleep(0.5)

    # ── Pipeline Summary ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  📊 Pipeline Summary")
    print("=" * 60)

    success = sum(1 for r in all_results if r["status"] == "success")
    failed  = len(all_results) - success
    total_tokens = sum(r["tokens_used"] for r in all_results)

    print(f"  Tasks processed : {len(all_results)}")
    print(f"  ✅ Successful   : {success}")
    print(f"  ❌ Failed       : {failed}")
    print(f"  🔢 Total tokens : {total_tokens}")

    # Save all results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "batch_pipeline_output.json")
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n💾 Full output saved to: batch_pipeline_output.json")
    print("=" * 60)
