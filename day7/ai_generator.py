import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from day5 folder
dotenv_path = os.path.abspath(os.path.join(os.getcwd(), "..", "day5", ".env"))
load_dotenv(dotenv_path)

def generate_pipeline():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in ../day5/.env")
        return

    client = Groq(api_key=api_key)
    
    prompt = """
    Create an advanced healthcare ETL pipeline using Python and Pandas that:
    - Reads patient CSV data from 'patients.csv'
    - Implements comprehensive LOGGING to a file 'pipeline.log' and console.
    - Cleans data: Removes duplicates, handles nulls (fill missing 'age' with mean, 'billing_amount' with 0).
    - Transformations:
        1. Aggregate total billing per 'diagnosis' AND 'hospital_id'.
        2. Generate daily patient counts based on 'visit_date'.
    - Schema Evolution: Ensure it can handle the new 'hospital_id' column seamlessly.
    - Adds robust error handling and detailed docstrings.
    - Saves the output to 'billing_enhanced.csv' and 'daily_enhanced.csv'.
    
    Provide only the Python code within a single code block.
    """

    print("Generating AI-powered pipeline using Llama 3.1 8B via Groq...")
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert data engineer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2048,
        )

        response_content = completion.choices[0].message.content
        
        # Extract code from response
        if "```python" in response_content:
            code = response_content.split("```python")[1].split("```")[0].strip()
        elif "```" in response_content:
            code = response_content.split("```")[1].split("```")[0].strip()
        else:
            code = response_content.strip()

        with open("ai_pipeline.py", "w") as f:
            f.write(code)
            
        print("AI-powered pipeline generated and saved to 'ai_pipeline.py'.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_pipeline()
