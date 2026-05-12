import pandas as pd
import os
import logging
from datetime import datetime

# Setup Alert Logging
logging.basicConfig(
    filename="notifications.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def trigger_alerts(input_path):
    """
    Reads the AI report and triggers alerts for Critical anomalies.
    """
    print(f"🔔 Starting Alerting Service on: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        return

    # 1. Load AI Report
    df = pd.read_csv(input_path)
    
    # 2. Filter for Critical Anomalies
    critical_anomalies = df[df["severity"] == "CRITICAL"]
    
    if critical_anomalies.empty:
        print("✅ No critical anomalies to alert.")
        return

    print(f"🚨 Triggering {len(critical_anomalies)} critical alerts...")
    
    for _, row in critical_anomalies.iterrows():
        alert_msg = f"""
        ---------- URGENT ANOMALY ALERT ----------
        Timestamp: {row['timestamp']}
        Revenue: ${row['revenue']}
        Severity: {row['severity']}
        AI Analysis: {row.get('ai_explanation', 'No AI analysis available.')}
        ------------------------------------------
        """
        # Log the "Email"
        logging.critical(alert_msg)
        print(f"📧 Alert sent for {row['timestamp']} (logged to notifications.log)")

    print(f"✅ Alerting service finished.")

if __name__ == "__main__":
    REPORT_FILE = "data/gold/anomalies_consolidated_report.csv"
    trigger_alerts(REPORT_FILE)
