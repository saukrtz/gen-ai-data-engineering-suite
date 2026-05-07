from agent import process_prompt

print("--- Interactive Snowflake AI Assistant ---")
print("Type 'exit' to quit.")

while True:
    user_input = input("\nAsk: ")
    
    if user_input.lower() in ['exit', 'quit']:
        break
        
    result = process_prompt(user_input)
    
    print("Result:", result)
