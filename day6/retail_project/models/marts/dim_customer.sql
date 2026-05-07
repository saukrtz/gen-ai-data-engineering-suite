SELECT DISTINCT
  customer_id,
  name,
  region
FROM {{ ref('stg_customers') }}
