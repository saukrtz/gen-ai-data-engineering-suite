import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Step 0: The Schema Knowledge
SCHEMA_CONTEXT = """
Source Tables (DAY6_GEN.F1ST):
- customers (customer_id, name, region)
- products (product_id, product_name, category)
- orders (order_id, customer_id, product_id, order_date, amount)
"""

def generate_model(prompt):
    """Calls Groq to generate dbt SQL code."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a dbt architect. Return ONLY valid SQL using Jinja templates. No markdown, no explanations."},
            {"role": "user", "content": f"Context: {SCHEMA_CONTEXT}\n\nTask: {prompt}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip().replace("```sql", "").replace("```", "")

def build_project():
    print("🚀 Starting Agentic dbt Build...")

    # 1. Generate Sources
    sources_yml = """version: 2
sources:
  - name: raw
    database: DAY6_GEN
    schema: F1ST
    tables:
      - name: customers
      - name: products
      - name: orders
"""
    os.makedirs("models", exist_ok=True)
    with open("models/sources.yml", "w") as f:
        f.write(sources_yml)
    print("✅ Created sources.yml")

    # 2. Generate Staging Models
    os.makedirs("models/staging", exist_ok=True)
    for table in ["customers", "products", "orders"]:
        print(f"-> Generating stg_{table}.sql...")
        sql = generate_model(f"Create a staging model for {table} using the source('raw', '{table}') function.")
        with open(f"models/staging/stg_{table}.sql", "w") as f:
            f.write(sql)

    # 3. Generate Marts (Dimensions & Facts)
    os.makedirs("models/marts", exist_ok=True)
    
    # Fact Sales
    print("-> Generating fact_sales.sql...")
    fact_sql = generate_model("Create a fact_sales model by joining stg_orders with stg_customers and stg_products. Include all order metrics.")
    with open("models/marts/fact_sales.sql", "w") as f:
        f.write(fact_sql)

    # Dim Customer
    print("-> Generating dim_customer.sql...")
    dim_sql = generate_model("Create a dim_customer model using stg_customers. Select distinct records.")
    with open("models/marts/dim_customer.sql", "w") as f:
        f.write(dim_sql)

    print("\n✨ Agentic dbt Project Built Successfully!")

if __name__ == "__main__":
    build_project()
