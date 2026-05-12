import pandas as pd
import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API key
ENV_PATH = "/Users/as-mac-1224/Documents/genai/data_pipeline/gen_ai/day5/.env"
load_dotenv(ENV_PATH)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def send_slack_alert(alert_data):
    """Mocks a Slack notification by logging to a file."""
    log_file = "slack_alerts.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(alert_data, indent=2) + "\n---\n")
    print(f"📩 Slack alert sent to {log_file}")

def analyze_failures_with_ai(report_path):
    """Processes DQ failures and generates AI-driven impact analysis."""
    if not os.path.exists(report_path):
        print(f"❌ Report {report_path} not found.")
        return

    df = pd.read_csv(report_path)
    failures = df[df["status"] == "FAIL"]

    if failures.empty:
        print("✅ No DQ violations found. System healthy.")
        return

    print(f"🤖 AI Incident Agent analyzing {len(failures)} violations...")

    for _, row in failures.iterrows():
        prompt = f"""
        System: You are an Expert Data Quality Engineer and Business Analyst.
        Task: Analyze the following data quality violation and explain the potential business impact.
        
        Violation Details:
        - Column: {row['column']}
        - Metric: {row['metric']}
        - Allowed Threshold: {row['threshold']}%
        - Actual Rate: {row['actual']}%
        - Static Severity: {row['severity']}
        
        Provide:
        1. Business Impact: (How this affects downstream apps/decisions)
        2. Remediation: (What the data team should do)
        3. Adjusted Severity: (Should it be higher or lower? Why?)
        
        Format the response as a short bulleted list.
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=300
            )
            ai_insight = completion.choices[0].message.content.strip()
            
            # Prepare Alert Data
            alert = {
                "type": "DATA_QUALITY_VIOLATION",
                "column": row['column'],
                "severity": row['severity'],
                "actual_null_rate": f"{row['actual']}%",
                "ai_impact_analysis": ai_insight
            }
            
            send_slack_alert(alert)
            
        except Exception as e:
            print(f"⚠️ AI Agent Error: {e}")

if __name__ == "__main__":
    REPORT_FILE = "data/audit/dq_report.csv"
    analyze_failures_with_ai(REPORT_FILE)
