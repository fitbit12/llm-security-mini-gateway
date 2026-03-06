import requests
import time
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"
def query_ollama(prompt):
    start = time.time()
    response = requests.post(
        OLLAMA_URL,
        json={
           "model": MODEL,
            "prompt": prompt,
            "stream": False  
        }
    )
    end=time.time()
    latency=(end-start)*1000
    result = response.json()
    return result["response"],latency
