import pandas as pd
import numpy as np
import os

def generate_sample_revenue_data(output_path):
    """
    Generates a dataset with intentional null values and schema inconsistencies
    to test the monitoring agent.
    """
    print("📊 Generating sample revenue data for monitoring...")
    
    data = {
        "revenue": [100, 200, np.nan, 400, np.nan, 600, 700, 800, 900, 1000], # 20% null (Threshold: 5%)
        "customer_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], # 0% null (Threshold: 2%)
        "region": ["North", "South", None, "West", "East", "North", "South", "West", "East", None], # 20% null (Threshold: 10%)
        "transaction_date": ["2024-01-01"] * 9 + [None] # 10% null (Threshold: 0.1%)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"✅ Data generated and saved to: {output_path}")
    print(f"🔍 Null counts:\n{df.isnull().sum()}")
    
    return df

if __name__ == "__main__":
    DATA_PATH = "data/source/raw_data.csv"
    generate_sample_revenue_data(DATA_PATH)
