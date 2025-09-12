import requests
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY")
print("DEBUG API_KEY:", "Loaded" if API_KEY else "Not found")

if not API_KEY:
    raise ValueError(" Missing PERPLEXITY_API_KEY. Please set it in your .env or system environment.")

def call_perplexity(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    return data["choices"][0]["message"]["content"]
