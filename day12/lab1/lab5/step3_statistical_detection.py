import pandas as pd
import numpy as np
import os

def run_statistical_detection(input_path, output_path):
    """
    Applies Z-Score detection and creates an ensemble gold layer.
    """
    print(f"📈 Starting Statistical Detection (Gold Layer) on: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found. Please run Step 2 first.")
        return

    # 1. Load Flagged Data
    df = pd.read_csv(input_path)
    
    # 2. Z-Score Calculation
    mean_rev = df["revenue"].mean()
    std_rev = df["revenue"].std()
    
    df["z_score"] = (df["revenue"] - mean_rev) / std_rev
    df["is_stat_anomaly"] = df["z_score"].apply(lambda x: 1 if abs(x) > 3 else 0)
    
    # 3. Ensemble Severity Logic
    # High = Both ML and Stat flag it
    # Medium = Only one flags it
    # Low = None
    def calculate_severity(row):
        if row["is_ml_anomaly"] == 1 and row["is_stat_anomaly"] == 1:
            return "CRITICAL"
        elif row["is_ml_anomaly"] == 1 or row["is_stat_anomaly"] == 1:
            return "WARNING"
        else:
            return "NORMAL"

    df["severity"] = df.apply(calculate_severity, axis=1)
    
    # 4. Save to Gold Layer
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    critical_count = len(df[df["severity"] == "CRITICAL"])
    warning_count = len(df[df["severity"] == "WARNING"])
    
    print(f"✅ Gold Layer Processing complete.")
    print(f"🚨 Anomalies Found: {critical_count} Critical, {warning_count} Warning.")
    print(f"💾 Results saved to: {output_path}")

if __name__ == "__main__":
    SILVER_FILE = "data/silver/revenue_flagged.csv"
    GOLD_FILE = "data/gold/anomalies_consolidated.csv"
    run_statistical_detection(SILVER_FILE, GOLD_FILE)
