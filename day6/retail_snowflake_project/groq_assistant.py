import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Load env file from the lab_optimization directory as mentioned by the user
load_dotenv("/Users/as-mac-1224/Documents/genai/data_pipeline/gen_ai/day6/lab_optimization/.env")

def ask_groq(prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # We will use llama-3.1-8b-instant as requested
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert Data Engineer. Be concise, direct, and output exactly what is asked without extra conversational filler."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python groq_assistant.py 'prompt'")
        sys.exit(1)
        
    prompt_text = sys.argv[1]
    print(ask_groq(prompt_text))
