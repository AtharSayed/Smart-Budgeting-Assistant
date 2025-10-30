import httpx
import json

OLLAMA_URL = "http://ollama:11434/api/generate"

def query_llm(prompt: str) -> str:
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    with httpx.Client(timeout=60.0) as client:
        response = client.post(OLLAMA_URL, json=payload)
        return response.json()["response"]