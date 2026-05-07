-- AI Generated Dimension Model (v2)
SELECT 
    customer_id,
    customer_name_clean AS name,
    region
FROM {{ ref('stg_v2_customers') }}
