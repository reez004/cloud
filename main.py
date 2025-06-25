from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = FastAPI()

# Enable CORS (for Flutter communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Define the /chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.message

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistralai/mistral-small",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that speaks Malayalam."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 100
            },
        )

        data = response.json()

        if "choices" in data:
            return {"response": data["choices"][0]["message"]["content"].strip()}
        else:
            print("❌ API Error:", data)
            return {"error": f"Unexpected response format: {data}"}

    except Exception as e:
        return {"error": str(e)}
