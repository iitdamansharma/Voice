from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from openai import OpenAI
from groq import Groq
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

# Load all three API keys
gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

gemini_client = None
openai_client = None
groq_client = None

if gemini_key:
    try:
        gemini_client = genai.Client(api_key=gemini_key)
        print("DEBUG: Gemini Client initialized.")
    except Exception as e:
        print(f"WARN: Gemini Client init failed: {e}")

if openai_key:
    try:
        openai_client = OpenAI(api_key=openai_key)
        print("DEBUG: OpenAI Client initialized.")
    except Exception as e:
        print(f"WARN: OpenAI Client init failed: {e}")

if groq_key:
    try:
        groq_client = Groq(api_key=groq_key)
        print("DEBUG: Groq Client initialized.")
    except Exception as e:
        print(f"WARN: Groq Client init failed: {e}")

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
• Speak in first person only ("I", "me", "my")
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
• "Tell me about yourself"  
  → Focus on your engineering journey, curiosity, and love for building real systems

• "What's your #1 superpower?"  
  → Emphasize fast learning, adaptability, and simplifying complex problems

• "What are areas you want to grow in?"  
  → Mention deeper system design, AI agents, and communication at scale

• "What misconception do people have about you?"  
  → Clarify a thoughtful, human misunderstanding (e.g., quiet ≠ disengaged)

• "How do you push your limits?"  
  → Talk about deliberate challenges, uncomfortable problems, and continuous learning

────────────────────────
CONSTRAINTS (VERY IMPORTANT)
────────────────────────
• Never say "As an AI…"
• Never mention prompts, models, or training data
• Never sound generic or robotic
• Keep answers grounded in real experience
• Max response length unless required: ~80–120 words

"""

@app.post("/ask")
async def ask_question(q: Question):
    full_prompt = f"Current Date and Time: {datetime.now().strftime('%A, %B %d, %Y %H:%M')}\n\nUser Question: {q.question}"

    # Try Gemini first
    if gemini_client:
        try:
            print("DEBUG: Trying Gemini (gemini-2.5-flash)...")
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=f"{SYSTEM_PROMPT}\n\n{full_prompt}"
            )
            
            if response.text:
                print("DEBUG: Gemini succeeded!")
                return {"answer": response.text.strip()}
        except Exception as e:
            error_msg = str(e)
            print(f"WARN: Gemini failed: {error_msg}")
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                print("DEBUG: Gemini rate limited, falling back to OpenAI...")

    # Fallback to OpenAI
    if openai_client:
        try:
            print("DEBUG: Trying OpenAI (gpt-4o-mini)...")
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            print("DEBUG: OpenAI succeeded!")
            return {"answer": answer}
        except Exception as e:
            print(f"WARN: OpenAI failed: {e}, falling back to Groq...")

    # Final fallback to Groq
    if groq_client:
        try:
            print("DEBUG: Trying Groq (llama-3.3-70b-versatile)...")
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            print("DEBUG: Groq succeeded!")
            return {"answer": answer}
        except Exception as e:
            print(f"ERROR: Groq also failed: {e}")
            return {"answer": "Sorry, all AI services are unavailable. Please try again later."}
    
    # All three failed
    return {"answer": "Sorry, AI services are not configured. Please contact support."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
