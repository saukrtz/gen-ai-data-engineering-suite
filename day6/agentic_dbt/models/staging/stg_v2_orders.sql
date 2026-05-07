-- AI Generated Staging Model (v2)
-- Using Jinja source function for raw connectivity
WITH raw_orders AS (
    SELECT * FROM {{ source('raw', 'orders') }}
)
SELECT 
    order_id,
    customer_id,
    product_id,
    order_date,
    amount,
    -- AI Insight: Calculating tax as a placeholder logic
    amount * 0.10 AS tax_amount,
    amount + (amount * 0.10) AS total_amount_with_tax
FROM raw_orders
