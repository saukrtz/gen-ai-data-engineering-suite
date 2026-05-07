-- AI Generated Dimension Model (v2)
SELECT 
    product_id,
    product_name,
    category,
    category_priority
FROM {{ ref('stg_v2_products') }}
