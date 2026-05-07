import sys
import os
import logging

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from prefect import flow, task
from pyspark.sql import SparkSession
from pipeline.bronze.ingest import BronzeIngestion
from pipeline.silver.process import SilverProcessor
from pipeline.gold.aggregate import GoldAggregator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@task(name="Bronze_Ingestion")
def run_bronze(spark):
    logger.info("Starting Bronze Layer Task")
    ingestion = BronzeIngestion(spark)
    ingestion.run("data/patients.csv", "output/bronze")

@task(name="Silver_Processing")
def run_silver(spark):
    logger.info("Starting Silver Layer Task")
    processor = SilverProcessor(spark)
    processor.run("output/bronze", "output/silver")

@task(name="Gold_Aggregation")
def run_gold(spark):
    logger.info("Starting Gold Layer Task")
    aggregator = GoldAggregator(spark)
    aggregator.run("output/silver", "output/gold")

@flow(name="Healthcare_Medallion_Pipeline")
def healthcare_pipeline():
    # Setup Spark once for the entire flow
    spark = SparkSession.builder \
        .appName("HealthcarePipeline") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    try:
        # Orchestrate tasks
        run_bronze(spark)
        run_silver(spark)
        run_gold(spark)
        logger.info("Pipeline completed successfully!")
    finally:
        spark.stop()

if __name__ == "__main__":
    healthcare_pipeline()
