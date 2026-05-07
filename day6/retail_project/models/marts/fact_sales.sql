SELECT 
  o.order_id,
  o.customer_id,
  o.product_id,
  o.order_date,
  o.amount
FROM {{ ref('stg_orders') }} o
