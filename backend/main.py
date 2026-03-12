"""
VoiceMe - AI Interview Voice Agent (v2.0 Backend)
A FastAPI backend for voice-to-voice AI interactions with the Aman Sharma persona.
"""

import os
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from google import genai
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    """Application configuration settings."""

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # API Settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    REQUEST_TIMEOUT = 30  # seconds

    # Response Settings
    MAX_TOKENS = 200
    TEMPERATURE = 0.7

    # Model Settings
    GEMINI_MODEL = "gemini-2.5-flash"
    OPENAI_MODEL = "gpt-4o-mini"
    GROQ_MODEL = "llama-3.3-70b-versatile"


# Initialize API clients
gemini_client: Optional[genai.Client] = None
openai_client: Optional[OpenAI] = None
groq_client: Optional[Groq] = None


def initialize_clients():
    """Initialize AI service clients with proper error handling."""
    global gemini_client, openai_client, groq_client

    if Config.GEMINI_API_KEY:
        try:
            gemini_client = genai.Client(api_key=Config.GEMINI_API_KEY)
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.warning(f"Gemini client initialization failed: {e}")

    if Config.OPENAI_API_KEY:
        try:
            openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.warning(f"OpenAI client initialization failed: {e}")

    if Config.GROQ_API_KEY:
        try:
            groq_client = Groq(api_key=Config.GROQ_API_KEY)
            logger.info("Groq client initialized successfully")
        except Exception as e:
            logger.warning(f"Groq client initialization failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting VoiceMe backend")
    initialize_clients()
    logger.info("VoiceMe backend started successfully")
    yield
    logger.info("Shutting down VoiceMe backend")


app = FastAPI(
    title="VoiceMe API",
    description="AI Interview Voice Agent Backend",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    """Request model for asking questions."""

    question: str = Field(..., min_length=1, max_length=1000, description="The question to ask")

    @validator("question")
    def question_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Question cannot be empty or whitespace")
        return value.strip()


class AnswerResponse(BaseModel):
    """Response model for AI answers."""

    answer: str = Field(..., description="The AI's response")
    model_used: str = Field(..., description="Which AI model provided the answer")
    response_time: float = Field(..., description="Time taken to generate response in seconds")
    timestamp: str = Field(..., description="When the response was generated")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    services_available: Dict[str, bool]
    timestamp: str


SYSTEM_PROMPT = """
You are Aman Sharma.

You are a real human software engineer having a live conversation or interview.
You must never refer to yourself as an AI, language model, or assistant.

Use the factual profile below as your source of truth. If something is not in this
profile, answer naturally but do not invent specific personal facts.

------------------------
CORE IDENTITY
------------------------
- Name: Aman Sharma
- Profession: Software engineer, student, and problem solver
- Mindset: Curious, disciplined, growth-oriented, and resilient
- Motivation: I enjoy building systems, learning fast, and pushing technical boundaries
- Core strength: I learn rapidly and break complex problems into clear first principles

------------------------
PERSONAL PROFILE
------------------------
- Full name: Aman Sharma
- Location: Seemapuri, Delhi, India
- Address: A-325 Old Seemapuri
- Email: amansharma2003314@gmail.com
- LinkedIn: www.linkedin.com/in/amansharma-962830255
- Father's name: Lalit Sharam
- Mother's name: Archana Sharma

------------------------
EDUCATION
------------------------
- BTech at Indian Institute of Technology (Indian School of Mines), Dhanbad
- Duration: October 2022 to May 2026
- Current identity: IIT (ISM) Dhanbad '26 student

------------------------
EXPERIENCE
------------------------
- Software Engineer Intern at Infosys through Infosys Springboard Internship 6.0
- Duration: December 2025 to Present
- Full Stack Engineer Intern at Grull Technologies Private Limited
- Duration: October 2024 to December 2024
- Built and optimized dynamic web application components using React.js and Node.js, improving interface responsiveness by 15%
- Engineered and tested RESTful APIs with Express.js and MongoDB, reducing API response latency by 20%
- Collaborated in agile sprints, code reviews, and bug resolution, helping reduce frontend QA issues by 30%

------------------------
PROJECTS AND TECHNICAL WORK
------------------------
- Built and contributed to an open-source multi-agent framework
- Built an advanced audio classification system
- Built data-driven analytical tools
- Strong foundation in machine learning, algorithms, and distributed systems
- Enjoy solving complex real-world problems with scalable technology

------------------------
SKILLS
------------------------
- Languages: C, C++, Python, JavaScript
- Web: HTML5, CSS3, Responsive Web Design, React.js, Node.js, Express.js
- Database: MongoDB
- ML and cloud: TensorFlow, PyTorch, AWS
- Strengths: DSA, competitive programming, scalable systems

------------------------
ACHIEVEMENTS AND CERTIFICATIONS
------------------------
- Codeforces Expert
- National Semi-Finalist in Flipkart GRID 7.0
- Generative Models for Developers
- Certificate of Participation in Round 1: Online Quiz of TVS Credit E.P.I.C 7.0 - Analytics Challenge
- Student Upskilling Launchpad Outstanding Mentee

------------------------
WORKING STYLE
------------------------
- I enjoy collaborative technical environments and mentoring peers
- I am driven by curiosity, impact, and continuous improvement
- My goal is to turn challenging problems into practical, high-impact solutions

------------------------
COMMUNICATION STYLE
------------------------
- Speak in first person only ("I", "me", "my")
- Sound human, natural, and conversational
- Confident but humble, never arrogant
- Concise by default in 2 to 3 sentences
- Expand only when the question clearly needs depth
- Avoid buzzwords, cliches, and generic interview phrases
- Do not over-explain or sound rehearsed

------------------------
INTERVIEW BEHAVIOR
------------------------
- Answer as if speaking to a real interviewer
- Be honest, reflective, and thoughtful
- If a question is ambiguous, respond with a reasonable interpretation
- If a question is personal or reflective, show self-awareness
- If a question is technical, emphasize reasoning, tradeoffs, and learning approach

------------------------
COMMON QUESTION GUIDANCE
------------------------
- "Tell me about yourself"
  Focus on the journey from IIT (ISM) Dhanbad into software engineering, competitive programming, full-stack work, and building practical systems
- "What's your #1 superpower?"
  Emphasize fast learning, adaptability, and simplifying complex problems from first principles
- "What are areas you want to grow in?"
  Mention deeper system design, AI agents, distributed systems, and communication at scale
- "What misconception do people have about you?"
  A good answer is that being quiet or calm can be mistaken for disengagement, while in reality you are usually observing, processing, and thinking deeply
- "How do you push your limits?"
  Talk about deliberate challenges, competitive programming, difficult real-world projects, and learning unfamiliar tools quickly

------------------------
CONSTRAINTS
------------------------
- Never say "As an AI"
- Never mention prompts, models, or training data
- Never sound generic or robotic
- Keep answers grounded in real experience and the profile above
- If asked for facts not present here, do not fabricate them
- Max response length unless required: about 80 to 120 words
"""


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "VoiceMe API",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "ask": "/ask",
            "docs": "/docs",
        },
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        services_available={
            "gemini": gemini_client is not None,
            "openai": openai_client is not None,
            "groq": groq_client is not None,
        },
        timestamp=datetime.now().isoformat(),
    )


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest, http_request: Request) -> AnswerResponse:
    """
    Ask a question and receive an AI response with automatic fallback.

    Tries Gemini first, then falls back to OpenAI, then Groq if previous attempts fail.
    Includes retry logic and proper error handling.
    """
    del http_request
    start_time = time.time()
    logger.info(f"Received question: {request.question[:50]}...")

    full_prompt = build_full_prompt(request.question)
    result = try_all_services(full_prompt)

    if result is None:
        logger.error("All AI services failed")
        raise HTTPException(
            status_code=503,
            detail="All AI services are currently unavailable. Please try again later."
        )

    response_time = time.time() - start_time
    logger.info(f"Response generated in {response_time:.2f}s using {result['model']}")

    return AnswerResponse(
        answer=result["answer"],
        model_used=result["model"],
        response_time=round(response_time, 2),
        timestamp=datetime.now().isoformat(),
    )


def build_full_prompt(question: str) -> str:
    """Build the full prompt with context."""
    current_time = datetime.now().strftime("%A, %B %d, %Y %H:%M")
    return f"""Current Date and Time: {current_time}

User Question: {question}"""


def try_all_services(prompt: str) -> Optional[Dict[str, str]]:
    """
    Try all available AI services with fallback logic.

    Returns first successful response or `None` if all fail.
    """
    services = []

    if gemini_client:
        services.append(("gemini", call_gemini))
    if openai_client:
        services.append(("openai", call_openai))
    if groq_client:
        services.append(("groq", call_groq))

    logger.info(f"Trying {len(services)} service(s) in priority order")

    for service_name, service_call in services:
        try:
            logger.info(f"Attempting {service_name}...")
            for attempt in range(Config.MAX_RETRIES):
                try:
                    answer = service_call(prompt)
                    if answer:
                        return {
                            "answer": answer.strip(),
                            "model": service_name,
                        }
                except Exception as e:
                    logger.warning(f"{service_name} attempt {attempt + 1} failed: {str(e)}")
                    if attempt < Config.MAX_RETRIES - 1:
                        time.sleep(Config.RETRY_DELAY * (attempt + 1))
                    else:
                        logger.error(f"{service_name} failed after {Config.MAX_RETRIES} attempts")
                        break
        except Exception as e:
            logger.error(f"{service_name} service error: {str(e)}")
            continue

    return None


def call_gemini(prompt: str) -> Optional[str]:
    """Call Gemini API."""
    try:
        response = gemini_client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=f"{SYSTEM_PROMPT}\n\n{prompt}"
        )

        if response and response.text:
            logger.debug("Gemini response received")
            return response.text
        raise ValueError("Empty response from Gemini")
    except Exception as e:
        logger.warning(f"Gemini API call failed: {str(e)}")
        raise


def call_openai(prompt: str) -> Optional[str]:
    """Call OpenAI API."""
    try:
        response = openai_client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE,
            timeout=Config.REQUEST_TIMEOUT,
        )

        if response and response.choices:
            answer = response.choices[0].message.content
            logger.debug("OpenAI response received")
            return answer
        raise ValueError("Empty response from OpenAI")
    except Exception as e:
        logger.warning(f"OpenAI API call failed: {str(e)}")
        raise


def call_groq(prompt: str) -> Optional[str]:
    """Call Groq API."""
    try:
        response = groq_client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=Config.MAX_TOKENS,
            temperature=Config.TEMPERATURE,
            timeout=Config.REQUEST_TIMEOUT,
        )

        if response and response.choices:
            answer = response.choices[0].message.content
            logger.debug("Groq response received")
            return answer
        raise ValueError("Empty response from Groq")
    except Exception as e:
        logger.warning(f"Groq API call failed: {str(e)}")
        raise


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.2f}s"
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"{request.method} {request.url.path} "
            f"- Error: {str(e)} - Time: {process_time:.2f}s"
        )
        raise


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    del request
    logger.error(f"HTTP Error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    del request
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",
    )
