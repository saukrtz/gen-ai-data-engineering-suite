from agent import clinical_assistant_chat

def run_benchmarks():
    print("--- Phase 4: Clinical Benchmarks Testing ---")
    
    benchmarks = [
        {
            "category": "Analytical",
            "prompt": "Show average ICU stay duration in days.",
            "goal": "Verify AVG and DATEDIFF usage."
        },
        {
            "category": "Clinical Alert",
            "prompt": "Identify any patients with blood pressure over 140.",
            "goal": "Verify conditional filtering."
        },
        {
            "category": "Join-Based",
            "prompt": "Show patient names along with their latest recorded heart rate.",
            "goal": "Verify JOIN logic on patient_id."
        }
    ]
    
    for test in benchmarks:
        print(f"\n[TEST] Category: {test['category']}")
        print(f"User Prompt: {test['prompt']}")
        try:
            # Note: Server must be running for this to succeed
            answer = clinical_assistant_chat(test["prompt"])
            print(f"Assistant Response:\n{answer}")
        except Exception as e:
            print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    run_benchmarks()
