import pandas as pd
import numpy as np
import yaml
import os

class MonitoringEngine:
    def __init__(self, config_path):
        self.config_path = config_path
        self.rules = self._load_config()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('monitoring_rules', [])

    def run_checks(self, df):
        """Evaluates data against thresholds."""
        print("🔍 Running Data Quality checks against thresholds...")
        results = []
        
        for rule in self.rules:
            col = rule['column']
            threshold = rule['threshold']
            severity = rule['severity']
            
            # Calculate Null Rate
            null_count = df[col].isnull().sum()
            total_count = len(df)
            actual_rate = (null_count / total_count) * 100
            
            status = "PASS"
            if actual_rate > threshold:
                status = "FAIL"
            
            results.append({
                "column": col,
                "metric": "null_rate",
                "threshold": threshold,
                "actual": actual_rate,
                "status": status,
                "severity": severity
            })
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    CONFIG_PATH = "config/thresholds.yaml"
    DATA_FILE = "data/source/raw_data.csv"
    
    # 1. Initialize Engine
    engine = MonitoringEngine(CONFIG_PATH)
    
    # 2. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"❌ Source data not found at {DATA_FILE}. Please run step1 first.")
    else:
        df = pd.read_csv(DATA_FILE)
        
        # 3. Run Checks
        report = engine.run_checks(df)
        
        # 4. Print Report
        print("\n--- Data Quality Report ---")
        print(report)
        
        # 5. Save results for the next stage
        os.makedirs("data/audit", exist_ok=True)
        report.to_csv("data/audit/dq_report.csv", index=False)
        print("\n✅ DQ Report saved to data/audit/dq_report.csv")
