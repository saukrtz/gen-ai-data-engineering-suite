{{
    config(
        materialized='table'
    )
}}

SELECT
    o.customer_id,
    c.name,
    p.category,
    SUM(o.amount) AS total_revenue,
    COUNT(*) AS total_orders
FROM {{ ref('stg_orders') }} AS o
INNER JOIN {{ ref('dim_customer') }} AS c
    ON o.customer_id = c.customer_id
INNER JOIN {{ ref('dim_product') }} AS p
    ON o.product_id = p.product_id
WHERE
    o.order_date >= DATE '2024-01-01'
GROUP BY
    o.customer_id,
    c.name,
    p.category
ORDER BY
    total_revenue DESC
