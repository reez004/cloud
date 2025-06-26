from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

# Put your Groq API key here directly OR use environment variables for security
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your-groq-api-key-here"

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set.")

app = FastAPI()

# CORS for frontend access (Flutter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.message

        # Send request to Groq API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that speaks Malayalam."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 200
            },
        )

        data = response.json()
        if "choices" in data:
            return {"response": data["choices"][0]["message"]["content"].strip()}
        else:
            return {"error": f"Unexpected response: {data}"}

    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Malayalam AI Backend is running ✅"}
