import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "gemma2-9b-it"

def classify_url(url):
    prompt = f"""
You are a cybersecurity assistant. Classify the following URL into one of these categories:

1. Phishing – Pretends to be a trusted site to steal personal data (e.g., login or banking).
2. Defacement – A legitimate website that has been altered or defaced by hackers.
3. Malicious – Delivers malware, spyware, or harmful code.
4. Benign – Safe, trusted website with no harmful behavior.

URL: {url}

Explain your reasoning clearly and return the final category at the end.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a cybersecurity assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()

        text = response.json()["choices"][0]["message"]["content"].strip()

        # Format the explanation
        lines = text.split("\n")
        lines = [line.strip() for line in lines if line.strip()]
        formatted_reason = "\n".join(lines)

        # Detect category
        category = None
        for cat in ["Phishing", "Defacement", "Malicious", "Benign"]:
            if cat.lower() in text.lower():
                category = cat
                break

        return category, formatted_reason

    except Exception as e:
        return "Error", f"Failed to classify URL: {str(e)}"
