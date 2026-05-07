-- AI Generated Fact Model (v2)
-- Aggregating Sales and Tax metrics
SELECT 
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.amount,
    o.tax_amount,
    o.total_amount_with_tax,
    c.region,
    p.category
FROM {{ ref('stg_v2_orders') }} o
LEFT JOIN {{ ref('stg_v2_customers') }} c ON o.customer_id = c.customer_id
LEFT JOIN {{ ref('stg_v2_products') }} p ON o.product_id = p.product_id
