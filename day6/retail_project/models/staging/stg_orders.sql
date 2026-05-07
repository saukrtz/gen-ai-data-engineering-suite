SELECT 
  order_id,
  customer_id,
  product_id,
  order_date,
  amount
FROM {{ source('raw','orders') }}
