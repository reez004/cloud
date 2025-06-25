from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

app = FastAPI()

# Enable CORS for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace * with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for chat
class ChatRequest(BaseModel):
    message: str

# POST /chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.message

        # Call OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
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
            return {"error": f"Unexpected response format: {data}"}

    except Exception as e:
        return {"error": str(e)}
