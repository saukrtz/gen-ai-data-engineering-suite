import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a PySpark script for the Bronze layer of a Medallion architecture.
Requirements:
1. Create a class 'BronzeIngestion'.
2. Method 'run' to ingest 'data/patients.csv' (header=True, inferSchema=True).
3. Write to 'output/bronze' in Delta format with overwrite mode.
4. Partition the data by 'visit_date'.
5. Configure the SparkSession for Delta Lake (extensions and catalog).
6. Include error handling and logging.
Output ONLY the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
