SELECT DISTINCT customer_id, name FROM {{ source('raw','customersv2') }}
