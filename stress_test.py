# stress_test.py — fires random prompts at Groq for 10 seconds to test rate limits
from groq import Groq
import os
import time
import random

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Pool of random prompts to cycle through
PROMPTS = [
    "What is a Python list comprehension? Answer in 1 sentence.",
    "What does SQL JOIN do? Answer in 1 sentence.",
    "What is a REST API? Answer in 1 sentence.",
    "What is a primary key in a database? Answer in 1 sentence.",
    "What is the difference between GET and POST? Answer in 1 sentence.",
    "What is a pandas DataFrame? Answer in 1 sentence.",
    "What does GROUP BY do in SQL? Answer in 1 sentence.",
    "What is a virtual environment in Python? Answer in 1 sentence.",
    "What is JSON? Answer in 1 sentence.",
    "What is an API key? Answer in 1 sentence.",
]

# ── Run for 10 seconds ───────────────────────────────────────────
DURATION = 10
start_time   = time.time()
call_count   = 0
success_count= 0
error_count  = 0
total_tokens = 0

print("=" * 55)
print(f"  🚀 Stress Test — sending prompts for {DURATION} seconds")
print("=" * 55)

while time.time() - start_time < DURATION:
    prompt = random.choice(PROMPTS)
    call_count += 1
    elapsed = round(time.time() - start_time, 1)

    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            max_tokens=50,    # keep it short — maximise request count
            messages=[{"role": "user", "content": prompt}]
        )
        tokens_used = resp.usage.total_tokens
        total_tokens += tokens_used
        success_count += 1
        print(f"  [{elapsed:05.1f}s] ✅ Call #{call_count:02} | tokens: {tokens_used:4} | prompt: {prompt[:45]}…")

    except Exception as e:
        error_count += 1
        # Capture the error type — likely RateLimitError when quota is hit
        print(f"  [{elapsed:05.1f}s] ❌ Call #{call_count:02} | ERROR: {type(e).__name__}: {str(e)[:60]}")
        time.sleep(1)    # back off for 1s before retrying

# ── Final Report ─────────────────────────────────────────────────
total_time = round(time.time() - start_time, 2)
print("\n" + "=" * 55)
print("  📊 Results")
print("=" * 55)
print(f"  Duration          : {total_time}s")
print(f"  Total calls made  : {call_count}")
print(f"  ✅ Successful     : {success_count}")
print(f"  ❌ Errors/limits  : {error_count}")
print(f"  Total tokens used : {total_tokens}")
print(f"  Avg tokens/call   : {round(total_tokens / max(success_count,1), 1)}")
print(f"  Calls/second      : {round(success_count / total_time, 2)}")
print("=" * 55)
