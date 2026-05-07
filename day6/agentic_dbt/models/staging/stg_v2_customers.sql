-- AI Generated Staging Model (v2)
WITH raw_customers AS (
    SELECT * FROM {{ source('raw', 'customers') }}
)
SELECT 
    customer_id,
    UPPER(name) AS customer_name_clean,
    region
FROM raw_customers
