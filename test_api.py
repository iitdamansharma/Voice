import requests
import json

url = "https://voice-2hoq.onrender.com/ask"
payload = {"question": "What is your name?"}

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
