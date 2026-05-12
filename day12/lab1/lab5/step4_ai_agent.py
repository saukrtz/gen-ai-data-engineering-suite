import pandas as pd
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from the day5 .env file
# Based on my earlier check, the .env is at: /Users/as-mac-1224/Documents/genai/data_pipeline/gen_ai/day5/.env
# But for portability, I'll try to load it from the current directory if it exists, otherwise use the absolute path.
ENV_PATH = "/Users/as-mac-1224/Documents/genai/data_pipeline/gen_ai/day5/.env"
load_dotenv(ENV_PATH)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_anomalies_with_ai(input_path, output_path):
    """
    Identifies flagged anomalies and asks Groq AI for an explanation.
    """
    print(f"🤖 Starting AI Root Cause Analysis (Gold+ Layer) on: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found. Please run Step 3 first.")
        return

    # 1. Load Gold Data
    df = pd.read_csv(input_path)
    
    # 2. Filter for Anomalies (Critical or Warning)
    anomalies = df[df["severity"] != "NORMAL"].copy()
    
    if anomalies.empty:
        print("✅ No anomalies found to analyze.")
        return

    print(f"🧠 Analyzing {len(anomalies)} anomalies using Llama 3.1 8b...")
    
    rca_results = []
    
    for idx, row in anomalies.iterrows():
        prompt = f"""
        System: You are a Senior Financial Data Auditor.
        Task: Analyze the following revenue anomaly and provide a 2-sentence Root Cause Analysis (RCA) and 1 recommended action.
        
        Data Point:
        - Timestamp: {row['timestamp']}
        - Revenue: ${row['revenue']}
        - Z-Score: {row['z_score']:.2f}
        - ML Flagged: {'Yes' if row['is_ml_anomaly'] == 1 else 'No'}
        - Severity: {row['severity']}
        
        Provide the output in this format:
        RCA: [Explanation]
        Action: [Recommendation]
        """
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )
            explanation = completion.choices[0].message.content.strip()
            rca_results.append(explanation)
        except Exception as e:
            print(f"⚠️ AI Error for index {idx}: {e}")
            rca_results.append("AI analysis failed.")

    # 3. Append results to the dataframe
    anomalies["ai_explanation"] = rca_results
    
    # Merge back to original df or save as a separate report
    report_path = output_path.replace(".csv", "_report.csv")
    anomalies.to_csv(report_path, index=False)
    
    print(f"✅ AI Analysis complete.")
    print(f"📝 Full report saved to: {report_path}")

if __name__ == "__main__":
    GOLD_FILE = "data/gold/anomalies_consolidated.csv"
    run_ai_analysis = True # Toggle to prevent accidental API costs
    if run_ai_analysis:
        analyze_anomalies_with_ai(GOLD_FILE, GOLD_FILE)
