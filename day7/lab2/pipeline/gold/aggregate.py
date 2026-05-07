import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

try:
    from delta.tables import DeltaTable
except ImportError:
    # If Delta isn't available, we'll use standard Spark writes as a fallback
    DeltaTable = None

class GoldAggregator:
    def __init__(self, spark):
        self.spark = spark
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run(self, input_path, output_path):
        try:
            self.logger.info(f"Reading from Silver layer at {input_path}")
            silver_df = self.spark.read.format("delta").load(input_path)

            # Step 7: Gold Layer (Aggregation)
            self.logger.info("Aggregating billing by diagnosis")
            gold_df = silver_df.groupBy("diagnosis") \
                .agg(F.sum("billing_amount").alias("total_billing"))

            # Step 9: Idempotent Design (MERGE)
            # Create output directory if it doesn't exist
            if not os.path.exists(output_path):
                self.logger.info(f"Creating new Gold table at {output_path}")
                gold_df.write.format("delta").mode("overwrite").save(output_path)
            else:
                self.logger.info(f"Merging updates into Gold table at {output_path}")
                target_table = DeltaTable.forPath(self.spark, output_path)
                
                target_table.alias("t").merge(
                    gold_df.alias("s"),
                    "t.diagnosis = s.diagnosis"
                ).whenMatchedUpdate(set={
                    "total_billing": "s.total_billing"
                }).whenNotMatchedInsert(values={
                    "diagnosis": "s.diagnosis",
                    "total_billing": "s.total_billing"
                }).execute()
            
            self.logger.info("Gold aggregation completed successfully.")
        except Exception as e:
            self.logger.error(f"Error in Gold Aggregation: {str(e)}")
            raise

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("GoldLayer") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    aggregator = GoldAggregator(spark)
    aggregator.run("output/silver", "output/gold")
    spark.stop()
