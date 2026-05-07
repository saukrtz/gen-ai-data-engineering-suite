SELECT DISTINCT product_id, category FROM {{ source('raw','productsv2') }}
