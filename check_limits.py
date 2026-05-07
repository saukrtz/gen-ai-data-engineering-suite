# check_limits.py — reads rate limit info from Groq response headers
from groq import Groq
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Use with_raw_response to access HTTP headers alongside the normal response
raw = client.chat.completions.with_raw_response.create(
    model="llama-3.1-8b-instant",
    max_tokens=1,          # minimal tokens — just enough to get headers back
    messages=[
        {"role": "user", "content": "hi"}
    ]
)

# Parse headers
headers = raw.headers

print("=" * 50)
print(f"  Model: llama-3.1-8b-instant")
print("=" * 50)

# ── Request limits (how many API calls per minute) ──────────────
print("\n📦 Request Limits (calls/min):")
print(f"  Limit     : {headers.get('x-ratelimit-limit-requests', 'N/A')}")
print(f"  Remaining : {headers.get('x-ratelimit-remaining-requests', 'N/A')}")
print(f"  Resets in : {headers.get('x-ratelimit-reset-requests', 'N/A')}")

# ── Token limits (how many tokens per minute) ────────────────────
print("\n🔤 Token Limits (tokens/min):")
print(f"  Limit     : {headers.get('x-ratelimit-limit-tokens', 'N/A')}")
print(f"  Remaining : {headers.get('x-ratelimit-remaining-tokens', 'N/A')}")
print(f"  Resets in : {headers.get('x-ratelimit-reset-tokens', 'N/A')}")

# ── Request timing info ──────────────────────────────────────────
print("\n⏱️  Request Info:")
print(f"  Processing time : {headers.get('x-groq-processing-time', 'N/A')} ms")
print(f"  Request ID      : {headers.get('x-request-id', 'N/A')}")
print("=" * 50)
