# 🛒 Retail Analytics System: Project Summary

## 1. Project Folder Structure
The following structure has been implemented in `gen_ai/day6/retail_project/`:
```text
models/
  staging/
    stg_customers.sql
    stg_products.sql
    stg_orders.sql
  marts/
    dim_customer.sql
    dim_product.sql
    fact_sales.sql
    schema.yml
  sources.yml
dbt_project.yml
```

## 2. Optimized SQL Queries (Steps 11-13)

### Step 11: General Optimization
*   **Original**: `SELECT * FROM orders`
*   **Optimized**:
    ```sql
    SELECT order_id, customer_id, amount 
    FROM orders;
    ```

### Step 12: NL2SQL (Total Revenue by Customer)
*   **Request**: "Total revenue by customer"
*   **Generated SQL**:
    ```sql
    SELECT 
        customer_id, 
        SUM(amount) as total_revenue
    FROM {{ ref('fact_sales') }}
    GROUP BY customer_id;
    ```

### Step 13: Advanced Optimization Task
*   **Original**: `SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id;`
*   **Improved (Staging + Filters + Structure)**:
    ```sql
    -- Using staging table for clean structure and filtering out non-revenue orders
    SELECT 
        customer_id, 
        SUM(amount) as total_revenue,
        COUNT(order_id) as total_orders
    FROM {{ ref('stg_orders') }}
    WHERE amount > 0 
    GROUP BY 1
    ORDER BY total_revenue DESC;
    ```

## 3. Final Execution Instructions
To complete the lab, please run the following commands in your terminal:

```bash
# Activate your dbt environment
source /Users/as-mac-1224/dbt-env/bin/activate

# Navigate to the project
cd /Users/as-mac-1224/Documents/genai/data_pipeline/gen_ai/day6/retail_project

# Run the models
dbt run

# Run the tests
dbt test
```

## 4. Validation Checklist
- [ ] **Data loads correctly**: Verify `fact_sales` is populated in Snowflake.
- [ ] **Tests pass**: `dbt test` should return all green.
- [ ] **Queries return correct results**: Run the optimized queries in Snowflake console.
- [ ] **No duplicates or nulls**: Ensured by `unique` and `not_null` tests in `schema.yml`.
