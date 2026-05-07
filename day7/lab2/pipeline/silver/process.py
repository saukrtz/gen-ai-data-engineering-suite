import logging
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

class SilverProcessor:
    def __init__(self, spark):
        self.spark = spark
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run(self, input_path, output_path):
        try:
            self.logger.info(f"Reading from Bronze layer at {input_path}")
            df = self.spark.read.format("delta").load(input_path)

            # Step 5: Silver Layer (Cleaning)
            self.logger.info("Cleaning data: Filling nulls and dropping duplicates")
            
            # 1. Fill null billing_amount with 0
            df = df.fillna({"billing_amount": 0})
            
            # 2. Drop duplicate patient_id records
            df = df.dropDuplicates(["patient_id"])

            # Step 10: Writing with mergeSchema support
            self.logger.info(f"Writing to Silver layer at {output_path}")
            df.write.format("delta") \
                .mode("overwrite") \
                .option("mergeSchema", "true") \
                .save(output_path)
            
            self.logger.info("Silver processing completed successfully.")
        except Exception as e:
            self.logger.error(f"Error in Silver Processing: {str(e)}")
            raise

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("SilverLayer") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    processor = SilverProcessor(spark)
    processor.run("output/bronze", "output/silver")
    spark.stop()
