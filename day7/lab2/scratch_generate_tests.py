import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a pytest script for a PySpark Medallion pipeline.
Requirements:
1. Use a pytest fixture to create a SparkSession.
2. Define a test 'test_silver_logic':
   - Create a small input DataFrame with:
     - Record 1: patient_id=1, billing_amount=100
     - Record 2: patient_id=1, billing_amount=200 (duplicate ID)
     - Record 3: patient_id=2, billing_amount=None (null amount)
   - Apply the Silver layer logic: fillna(0) for billing_amount and dropDuplicates(['patient_id']).
   - Assert:
     - The result has 2 rows.
     - The null billing_amount is now 0.
Only output the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
