import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a PySpark script for the Silver layer of a Medallion architecture.
Requirements:
1. Create a class 'SilverProcessor'.
2. Method 'run' to read from 'output/bronze' (Delta format).
3. Cleaning Logic:
   - Fill null 'billing_amount' with 0.
   - Drop duplicate 'patient_id' records.
   - Handle potential nulls in 'name' or 'diagnosis' with "Unknown".
4. Write to 'output/silver' in Delta format with overwrite mode.
5. Support schema evolution by adding the 'mergeSchema' option.
6. Include a SparkSession builder with Delta Lake configurations.
7. Include logging and error handling.
Output ONLY the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
