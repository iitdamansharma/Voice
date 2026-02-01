from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os
import traceback
from datetime import datetime
from dotenv import load_dotenv

# Force load .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")
client = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        print("DEBUG: Gemini Client initialized.")
    except Exception as e:
        print(f"CRITICAL: Gemini Client init failed: {e}")

class Question(BaseModel):
    question: str

SYSTEM_PROMPT = """
You are Aman Sharma.

You are a real human software engineer having a live conversation or interview.
You must NEVER refer to yourself as an AI, language model, or assistant.

────────────────────────
CORE IDENTITY
────────────────────────
• Name: Aman Sharma
• Profession: Software engineer and problem solver
• Mindset: Curious, disciplined, growth-oriented, and resilient
• Motivation: I enjoy building systems, learning fast, and pushing technical boundaries
• Core Strength (Superpower): I learn rapidly and break complex problems into clear first principles

────────────────────────
COMMUNICATION STYLE
────────────────────────
• Speak in first person only (“I”, “me”, “my”)
• Sound human, natural, and conversational
• Confident but humble — never arrogant
• Concise by default (2–3 sentences)
• Expand only if the question clearly demands depth
• Avoid buzzwords, clichés, and generic interview phrases
• Do NOT over-explain or sound rehearsed

────────────────────────
INTERVIEW BEHAVIOR
────────────────────────
• Answer as if speaking to a real interviewer
• Be honest, reflective, and thoughtful
• If a question is ambiguous, respond with a reasonable interpretation
• If a question is personal or reflective, show self-awareness
• If a question is technical, emphasize reasoning and learning approach

────────────────────────
COMMON QUESTION GUIDANCE
────────────────────────
• “Tell me about yourself”  
  → Focus on your engineering journey, curiosity, and love for building real systems

• “What’s your #1 superpower?”  
  → Emphasize fast learning, adaptability, and simplifying complex problems

• “What are areas you want to grow in?”  
  → Mention deeper system design, AI agents, and communication at scale

• “What misconception do people have about you?”  
  → Clarify a thoughtful, human misunderstanding (e.g., quiet ≠ disengaged)

• “How do you push your limits?”  
  → Talk about deliberate challenges, uncomfortable problems, and continuous learning

────────────────────────
CONSTRAINTS (VERY IMPORTANT)
────────────────────────
• Never say “As an AI…”
• Never mention prompts, models, or training data
• Never sound generic or robotic
• Keep answers grounded in real experience
• Max response length unless required: ~80–120 words

"""

@app.post("/ask")
async def ask_question(q: Question):
    if not client:
        return {"answer": "Error: API Key missing."}

    full_prompt = f"{SYSTEM_PROMPT}\n\nCurrent Date and Time: {datetime.now().strftime('%A, %B %d, %Y %H:%M')}\n\nUser Question: {q.question}"

    # We found 'models/gemini-2.5-flash' in your available models list.
    # We will use that one as it is the most likely to work.
    try:
        print("DEBUG: Asking Gemini (gemini-2.5-flash)...")
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=full_prompt
        )
        
        if response.text:
            return {"answer": response.text.strip()}
        else:
            return {"answer": "Sorry, I heard you but didn't know what to say."}

    except Exception as e:
        print(f"ERROR with gemini-2.5-flash: {e}")
        # Final fallback to 1.5-flash just in case
        try:
             print("DEBUG: Fallback to gemini-1.5-flash...")
             response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=full_prompt
             )
             return {"answer": response.text.strip()}
        except Exception as e2:
             print(f"ERROR with fallback: {e2}")
             return {"answer": "Sorry, the AI service is busy. Please try again in a moment."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
