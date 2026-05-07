# csv_analyst.py — reads Customers, Orders, Products CSVs and sends combined data to Llama for analysis
from groq import Groq
import pandas as pd
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ── Paths ─────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)
customers_df = pd.read_csv(os.path.join(BASE, "Customers.csv"))
orders_df    = pd.read_csv(os.path.join(BASE, "Orders.csv"))
products_df  = pd.read_csv(os.path.join(BASE, "Products.csv"))

# ── Join all three tables into one view ───────────────────────────
# Orders ← Customers (on customer_id) ← Products (on product_id)
merged = (
    orders_df
    .merge(customers_df, on="customer_id", how="left")
    .merge(products_df,  on="product_id",  how="left")
)

# ── Build a summary for the LLM ───────────────────────────────────
# Convert the merged table to a readable string
data_str = merged[[
    "order_id", "name", "region", "product_name", "category", "amount", "order_date"
]].to_string(index=False)

# Quick aggregate stats to include in the prompt
total_revenue  = merged["amount"].sum()
avg_order      = merged["amount"].mean()
top_customer   = merged.groupby("name")["amount"].sum().idxmax()
top_product    = merged.groupby("product_name")["amount"].sum().idxmax()
top_region     = merged.groupby("region")["amount"].sum().idxmax()

# ── Compose the prompt ────────────────────────────────────────────
prompt = f"""
You are an agent.

Question: Find top selling product.

You have access to the following sales data (Customers + Orders + Products joined):

{data_str}

Quick Stats available to you:
- Total Revenue    : ₹{total_revenue}
- Avg Order Value  : ₹{avg_order:.2f}
- Top Customer     : {top_customer}
- Best Selling Product (by revenue) : {top_product}
- Top Region       : {top_region}

Follow this exact reasoning format:

Thought: (reason about what data to look at)
Action: (describe what calculation or lookup you perform)
Observation: (state what you found from the data)
Answer: (give the final clear answer)
"""

print("=" * 60)
print("  🤖 Agent-Style Reasoning — Finding Top Selling Product")
print("=" * 60)
print(f"\n📄 Data Preview:\n{data_str}\n")
print("=" * 60)
print("\n🧠 Llama Agent Reasoning (Thought → Action → Observation → Answer):\n")

# ── Send to Groq / Llama ──────────────────────────────────────────
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    max_tokens=600,
    messages=[
        {
            "role": "system",
            "content": (
                "You are an intelligent data agent. "
                "When answering questions, always reason step by step using this exact format:\n"
                "Thought: <your reasoning>\n"
                "Action: <what you look up or calculate>\n"
                "Observation: <what the data shows>\n"
                "Answer: <your final conclusion>\n"
                "Do not skip any step."
            )
        },
        {"role": "user", "content": prompt}
    ]
)

print(response.choices[0].message.content)
print(f"\n✅ Tokens used: {response.usage.total_tokens}")
print("=" * 60)
