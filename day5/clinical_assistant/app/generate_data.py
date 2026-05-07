import pandas as pd
from datetime import datetime, timedelta
import random

def generate_clinical_data():
    print("--- Generating Synthetic Clinical Data ---")
    
    # 1. Patients Data
    patients = [
        [101, "John Doe", 45, "M", "Hypertension"],
        [102, "Jane Smith", 32, "F", "Type 2 Diabetes"],
        [103, "Alice Johnson", 68, "F", "Congestive Heart Failure"],
        [104, "Bob Brown", 55, "M", "COPD"],
        [105, "Charlie Davis", 29, "M", "Acute Appendicitis"]
    ]
    df_patients = pd.DataFrame(patients, columns=["patient_id", "name", "age", "gender", "diagnosis"])
    df_patients.to_csv("gen_ai/clinical_assistant/data/patients.csv", index=False)
    
    # 2. Admissions Data
    admissions = [
        [501, 101, "2024-01-10", "2024-01-15", "Cardiology"],
        [502, 102, "2024-02-01", "2024-02-05", "General Medicine"],
        [503, 103, "2024-01-20", "2024-01-30", "ICU"],
        [504, 104, "2024-03-15", "2024-03-20", "Pulmonology"],
        [505, 105, "2024-04-01", "2024-04-03", "Surgery"]
    ]
    df_admissions = pd.DataFrame(admissions, columns=["admission_id", "patient_id", "admission_date", "discharge_date", "department"])
    df_admissions.to_csv("gen_ai/clinical_assistant/data/admissions.csv", index=False)
    
    # 3. Vitals Data
    vitals = []
    for patient_id in [101, 102, 103, 104, 105]:
        for i in range(5): # 5 readings each
            bp = random.randint(110, 160)
            hr = random.randint(60, 100)
            timestamp = datetime(2024, 1, 1) + timedelta(days=i, hours=random.randint(0, 23))
            vitals.append([patient_id, bp, hr, timestamp.strftime("%Y-%m-%d %H:%M:%S")])
            
    df_vitals = pd.DataFrame(vitals, columns=["patient_id", "bp", "heart_rate", "recorded_at"])
    df_vitals.to_csv("gen_ai/clinical_assistant/data/vitals.csv", index=False)
    
    print("✅ CSV files generated in gen_ai/clinical_assistant/data/")

if __name__ == "__main__":
    generate_clinical_data()
