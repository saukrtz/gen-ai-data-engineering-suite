import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

RAW_QUERY = """
SELECT c.customer_id, c.name, p.category, SUM(o.amount) AS total_revenue, COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.name, p.category
ORDER BY total_revenue DESC;
"""

def call_agent(task, query):
    """General function to call the Groq Agent."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a Senior Data Engineer. Answer the user's task precisely and professionally."},
            {"role": "user", "content": f"Task: {task}\n\nSQL Query:\n{query}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def run_lab():
    print("🚀 STARTING LAB OPTIMIZATION AGENT...")
    print("="*50)

    # Step 3: Explain Query
    print("\n[Step 3] AI -> Explain Query (Plain English)")
    explanation = call_agent("Explain this SQL query in simple English.", RAW_QUERY)
    print(explanation)

    # Step 4: Optimize Query
    print("\n" + "="*50)
    print("[Step 4] AI -> Optimize Query")
    optimized_query = call_agent("Optimize this SQL query for Snowflake performance and best practices.", RAW_QUERY)
    print(optimized_query)

    # Step 5: SQL Linting
    print("\n" + "="*50)
    print("[Step 5] AI -> SQL Code Linting (Simulating SQLFluff)")
    linted_query = call_agent("Lint this SQL query. Apply ANSI standards, fix indentation, and ensure consistent casing.", optimized_query)
    print(linted_query)

    # Step 6: Convert to dbt Model
    print("\n" + "="*50)
    print("[Step 6] AI -> Convert to dbt Model")
    dbt_model = call_agent("Convert this optimized SQL into a dbt model using ref() functions.", linted_query)
    print(dbt_model)

    # Step 8: Generate dbt Tests
    print("\n" + "="*50)
    print("[Step 8] AI -> Generate dbt Tests")
    dbt_tests = call_agent("Generate a schema.yml file with not_null, unique, and relationships tests for this model.", dbt_model)
    print(dbt_tests)

    print("\n" + "="*50)
    print("✨ LAB AGENT EXECUTION COMPLETE ✨")

if __name__ == "__main__":
    run_lab()
