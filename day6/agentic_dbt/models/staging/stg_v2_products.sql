-- AI Generated Staging Model (v2)
WITH raw_products AS (
    SELECT * FROM {{ source('raw', 'products') }}
)
SELECT 
    product_id,
    product_name,
    category,
    -- AI Insight: Logic for high-value categories
    CASE 
        WHEN category = 'Electronics' THEN 'High Priority'
        ELSE 'Standard'
    END AS category_priority
FROM raw_products
