import pandas as pd
from sklearn.ensemble import IsolationForest
import os

def run_ml_detection(input_path, output_path):
    """
    Reads the bronze dataset, applies Isolation Forest, and saves to silver.
    """
    print(f"🔍 Starting ML Detection (Silver Layer) on: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found. Please run Step 1 first.")
        return

    # 1. Load Data
    df = pd.read_csv(input_path)
    
    # 2. Initialize Isolation Forest
    # contamination='auto' calculates the threshold based on the data
    model = IsolationForest(contamination=0.01, random_state=42)
    
    # 3. Fit and Predict
    # Isolation Forest returns -1 for outliers and 1 for inliers
    df["ml_anomaly_score"] = model.fit_predict(df[["revenue"]])
    
    # Convert to more readable format: 1 for anomaly, 0 for normal
    df["is_ml_anomaly"] = df["ml_anomaly_score"].apply(lambda x: 1 if x == -1 else 0)
    
    # 4. Save to Silver Layer
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    num_anomalies = df["is_ml_anomaly"].sum()
    print(f"✅ ML Detection complete. Found {num_anomalies} anomalies.")
    print(f"💾 Results saved to: {output_path}")

if __name__ == "__main__":
    BRONZE_FILE = "data/bronze/revenue_raw.csv"
    SILVER_FILE = "data/silver/revenue_flagged.csv"
    run_ml_detection(BRONZE_FILE, SILVER_FILE)
