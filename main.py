from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class AIRequest(BaseModel):
    query: str

class AIResponse(BaseModel):
    answer: str

@app.post("/ai-chat", response_model=AIResponse)
async def chat_with_ai(request: AIRequest):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": request.query}]
    }
    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        return AIResponse(answer=result['choices'][0]['message']['content'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
