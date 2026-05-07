import pandas as pd

# Step 1: Load Data
df = pd.read_csv("patients.csv")

# Step 2: Data Cleaning
df = df.drop_duplicates()
df["age"] = df["age"].fillna(df["age"].mean())
df["billing_amount"] = df["billing_amount"].fillna(0)

# Step 3: Transformations
# Total Billing per Diagnosis
billing = df.groupby("diagnosis")["billing_amount"].sum()
# Daily Patient Count
daily = df.groupby("visit_date")["patient_id"].count()

# Step 4: Save Output
billing.to_csv("billing.csv")
daily.to_csv("daily.csv")

print("Traditional ETL completed successfully.")
print("\nBilling per Diagnosis:")
print(billing)
print("\nDaily Patient Count:")
print(daily)
