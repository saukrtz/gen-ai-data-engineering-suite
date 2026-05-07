import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder \
        .master("local[1]") \
        .appName("PipelineTests") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

def test_silver_cleaning_logic(spark):
    # Setup: Create dummy data for Step 5 (Silver cleaning)
    data = [
        (1, "Alice", 200.0),
        (1, "Alice", 500.0), # Duplicate patient_id
        (2, "Bob", None)     # Null billing_amount
    ]
    schema = ["patient_id", "name", "billing_amount"]
    df = spark.createDataFrame(data, schema)

    # Execution: Apply cleaning logic
    df_clean = df.fillna({"billing_amount": 0}).dropDuplicates(["patient_id"])
    
    # Assertions
    results = df_clean.collect()
    assert df_clean.count() == 2 # Duplicate removed
    
    bob_record = [r for r in results if r.patient_id == 2][0]
    assert bob_record.billing_amount == 0 # Null filled

def test_gold_aggregation_logic(spark):
    # Setup: Create dummy data for Step 7 (Gold aggregation)
    data = [
        ("Diabetes", 200.0),
        ("Diabetes", 300.0),
        ("Cardiac", 500.0)
    ]
    schema = ["diagnosis", "billing_amount"]
    df = spark.createDataFrame(data, schema)
    
    # Execution: Apply aggregation
    df_gold = df.groupBy("diagnosis").agg(F.sum("billing_amount").alias("total_billing"))
    
    # Assertions
    results = {r.diagnosis: r.total_billing for r in df_gold.collect()}
    assert results["Diabetes"] == 500.0
    assert results["Cardiac"] == 500.0
