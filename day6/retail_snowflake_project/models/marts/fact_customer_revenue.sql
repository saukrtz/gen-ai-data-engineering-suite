SELECT 
    o.customer_id,
    c.name,
    p.category,
    SUM(o.amount) AS total_revenue,
    COUNT(*) AS total_orders
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('dim_customer') }} c 
    ON o.customer_id = c.customer_id
JOIN {{ ref('dim_product') }} p 
    ON o.product_id = p.product_id
GROUP BY o.customer_id, c.name, p.category
