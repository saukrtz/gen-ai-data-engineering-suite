import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class BronzeIngestion:
    def __init__(self, spark):
        self.spark = spark
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def run(self, input_file, output_dir, last_run_date=None):
        """
        Ingests CSV data into Bronze Delta layer with optional incremental filtering.
        """
        try:
            self.logger.info(f"Reading data from {input_file}")
            df = self.spark.read.csv(input_file, header=True, inferSchema=True)
            
            # Step 4: Incremental Ingestion Logic
            if last_run_date:
                self.logger.info(f"Filtering records newer than {last_run_date}")
                df = df.filter(col("visit_date") > last_run_date)
            
            count = df.count()
            if count == 0:
                self.logger.info("No new data to ingest.")
                return

            self.logger.info(f"Writing {count} records to Delta at {output_dir} partitioned by visit_date")
            
            # Using append mode for incremental ingestion to maintain history
            df.write.format("delta") \
                .mode("append") \
                .partitionBy("visit_date") \
                .save(output_dir)
            
            self.logger.info("Bronze ingestion completed successfully.")
        except Exception as e:
            self.logger.error(f"Error in Bronze Ingestion: {str(e)}")
            raise

if __name__ == "__main__":
    # SparkSession configured for Delta Lake
    spark = SparkSession.builder \
        .appName("BronzeLayer") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    ingestion = BronzeIngestion(spark)
    
    # Initial run (Full load)
    ingestion.run("data/patients.csv", "output/bronze")
    
    # Example of incremental call (commented out for now)
    # ingestion.run("data/patients.csv", "output/bronze", last_run_date="2024-01-01")
    
    spark.stop()
