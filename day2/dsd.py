# pip install groq
from groq import Groq
import os

# Initialise the Groq client — reads GROQ_API_KEY from environment
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Uses Llama 3 — fast, free, no quota issues
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "Explain what SQL GROUP BY does in 100 words"}
    ]
)

print(response.choices[0].message.content)
