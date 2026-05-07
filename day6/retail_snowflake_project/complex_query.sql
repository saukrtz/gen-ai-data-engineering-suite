-- Step 2: Complex 3-Join Query
SELECT 
    c.customer_id,
    c.name,
    p.category,
    SUM(o.amount) AS total_revenue,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY c.customer_id, c.name, p.category
ORDER BY total_revenue DESC;
