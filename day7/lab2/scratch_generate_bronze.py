import sys
import os

# Add the project root to sys.path to import utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a PySpark script for the Bronze layer of a Medallion architecture.
Requirements:
1. Create a class 'BronzeIngestion'.
2. Method 'run' to ingest 'data/patients.csv' (header=True, inferSchema=True).
3. Write to 'output/bronze' in Parquet format with overwrite mode.
4. Include a SparkSession builder with app name 'BronzeLayer'.
5. Include basic try-except error handling and print statements for logging.
Output ONLY the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
