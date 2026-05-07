import snowflake.connector
import os

# Using the credentials you provided from Day 5
conn = snowflake.connector.connect(
    user='DREAM',
    password='Sigmoid@202669',
    account='JGZAFOP-MJ33102',
    warehouse='COMPUTE_WH'
)

sql_commands = [
    "CREATE DATABASE IF NOT EXISTS day6_genv2",
    "CREATE SCHEMA IF NOT EXISTS day6_genv2.f1stv2",
    "USE DATABASE day6_genv2",
    "USE SCHEMA f1stv2",
    "CREATE OR REPLACE TABLE customersv2 (customer_id INT, name STRING, region STRING)",
    "CREATE OR REPLACE TABLE productsv2 (product_id INT, product_name STRING, category STRING)",
    "CREATE OR REPLACE TABLE ordersv2 (order_id INT, customer_id INT, product_id INT, order_date DATE, amount NUMBER)",
    "INSERT INTO customersv2 VALUES (1,'Alice','North'), (2,'Bob','South')",
    "INSERT INTO productsv2 VALUES (101,'Laptop','Electronics'), (102,'Phone','Electronics')",
    "INSERT INTO ordersv2 VALUES (1001, 1, 101, '2024-01-01', 500), (1002, 2, 102, '2024-01-02', 300), (1003, NULL, 101, '2024-01-03', 200)"
]

cursor = conn.cursor()
for cmd in sql_commands:
    print(f"Executing: {cmd}")
    cursor.execute(cmd)

conn.close()
print("Snowflake warehouse populated successfully with v2 tables!")
