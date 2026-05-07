import os
import requests
import json

class GroqLLM:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def generate_code(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a PySpark expert helping build a Medallion architecture pipeline. Output ONLY code, no explanations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1
        }
        
        try:
            response = requests.post(self.url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Error calling Groq API: {str(e)}"

if __name__ == "__main__":
    # Test call
    llm = GroqLLM()
    print(llm.generate_code("Create a simple SparkSession initialization code."))
