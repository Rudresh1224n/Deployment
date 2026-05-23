from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
load_dotenv()
import os

# =========================
# FASTAPI APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# OPENAI CLIENT
# =========================

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://apidev.navigatelabsai.com"
)

# =========================
# REQUEST MODEL
# =========================

class PromptRequest(BaseModel):
    user_prompt: str

# =========================
# ROUTES
# =========================

@app.get("/")
def read_root():
    return {"message": "NexusAI backend is running"}

@app.post("/run_task/")
async def run_task(req: PromptRequest):

    try:

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a personal AI tutor. "
                        "Explain the user's content in simple layman terms. "
                        "Keep responses short and precise. "
                        "Do not hallucinate."
                    )
                },
                {
                    "role": "user",
                    "content": req.user_prompt
                }
            ],
            max_tokens=500
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}