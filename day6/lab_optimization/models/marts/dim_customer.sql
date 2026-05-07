SELECT DISTINCT customer_id, name FROM {{ source('raw','customers') }}
