import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a PySpark script for the Gold layer of a Medallion architecture.
Requirements:
1. Create a class 'GoldAggregator'.
2. Method 'run' to read from 'output/silver' (Delta format).
3. Aggregation Logic:
   - Group by 'diagnosis'.
   - Aggregate sum of 'billing_amount' as 'total_billing'.
4. Idempotent Design (Step 9):
   - Use Delta MERGE to update 'output/gold' table.
   - Join on 'diagnosis'.
   - When matched, update 'total_billing'.
   - When not matched, insert the record.
5. Include a SparkSession builder with Delta Lake configurations.
6. Include logging and error handling.
Output ONLY the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
