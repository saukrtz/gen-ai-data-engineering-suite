import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_complex_dataset(output_path):
    """
    Generates a realistic 30-day hourly revenue dataset with injected anomalies.
    """
    print("🚀 Starting Data Synthesis (Bronze Layer)...")
    
    # Configuration
    np.random.seed(42)
    start_date = datetime(2024, 5, 1)
    num_hours = 24 * 30
    
    # 1. Generate Timestamps
    timestamps = [start_date + timedelta(hours=i) for i in range(num_hours)]
    
    # 2. Generate Base Revenue (Normal Distribution: Mean=150, SD=20)
    base_revenue = np.random.normal(loc=150, scale=20, size=num_hours)
    
    # 3. Add Seasonality (Daily Peak at Noon)
    for i in range(num_hours):
        hour = timestamps[i].hour
        # Simple sine-wave seasonality
        seasonality = 10 * np.sin(np.pi * (hour - 6) / 12)
        base_revenue[i] += seasonality

    df = pd.DataFrame({
        "timestamp": timestamps,
        "revenue": base_revenue.round(2)
    })

    # 4. Inject Anomalies
    # Extreme Spike (Global Anomaly)
    df.loc[100, "revenue"] = 5000.0  # Index 100
    
    # Extreme Drop (Global Anomaly)
    df.loc[250, "revenue"] = -50.0   # Index 250 (Impossible value)
    
    # High-Volume Spike (Contextual Anomaly)
    df.loc[400, "revenue"] = 800.0   # Index 400
    
    # Subtle Outlier
    df.loc[600, "revenue"] = 450.0   # Index 600

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save to Bronze Layer
    df.to_csv(output_path, index=False)
    print(f"✅ Dataset generated and saved to: {output_path}")
    print(f"📊 Total Records: {len(df)}")
    print(f"⚠️ Injected Anomalies at indices: [100, 250, 400, 600]")
    
    return df

if __name__ == "__main__":
    BRONZE_PATH = "data/bronze/revenue_raw.csv"
    generate_complex_dataset(BRONZE_PATH)
