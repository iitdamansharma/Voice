import os
import traceback

from groq import Groq

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

print(f"API key loaded: {bool(api_key)}")
print(f"Key prefix: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    print("Groq client initialized")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one word"},
        ],
        max_tokens=10,
        temperature=0.7,
    )

    answer = response.choices[0].message.content.strip()
    print(f"Groq API works. Response: {answer}")
except Exception as e:
    print("Groq failed")
    print(f"Error: {e}")
    print(f"Traceback:\n{traceback.format_exc()}")
