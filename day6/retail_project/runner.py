python3 -c "
import snowflake.connector
import os
import json

conn = snowflake.connector.connect(
    user='DREAM',
    password='Sigmoid@202669',
    account='JGZAFOP-MJ33102',
    warehouse='COMPUTE_WH',
    database='DAY6_GEN',
    schema='F1ST'
)
cursor = conn.cursor()
cursor.execute('SELECT * FROM FACT_SALES LIMIT 5')
columns = [col[0] for col in cursor.description]
print(f'Table: FACT_SALES')
print('-' * 20)
print(columns)
for row in cursor.fetchall():
    print(row)
conn.close()
"