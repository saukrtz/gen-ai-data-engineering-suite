import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pipeline')))

from utils.llm_helper import GroqLLM

prompt = """
Create a Prefect 2.0+ orchestration script for a PySpark Medallion pipeline.
Requirements:
1. Import 'BronzeIngestion' from 'pipeline.bronze.ingest'.
2. Import 'SilverProcessor' from 'pipeline.silver.process'.
3. Import 'GoldAggregator' from 'pipeline.gold.aggregate'.
4. Define 3 Prefect @task-decorated functions:
   - 'run_bronze': runs the bronze ingestion.
   - 'run_silver': runs the silver processing.
   - 'run_gold': runs the gold aggregation.
5. Define a @flow-decorated function 'healthcare_pipeline':
   - Sets up a single SparkSession with Delta Lake configs.
   - Orchestrates the tasks sequentially: Bronze -> Silver -> Gold.
   - Properly closes the SparkSession at the end.
6. Include basic logging.
Output ONLY the Python code.
"""

llm = GroqLLM()
code = llm.generate_code(prompt)
print(code)
