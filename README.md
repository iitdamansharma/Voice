# 🎙️ VoiceMe - AI Interview Voice Agent

**VoiceMe** is an interactive voice-based AI agent designed to simulate a real human conversation. It adopts the persona of **Aman Sharma**, a passionate software engineer, capable of answering interview questions with a distinct personality, resilience, and professional tone.

---

## 🚀 Features

- **🗣️ Voice-to-Voice Interaction**: Speak naturally to the bot, and it replies with a synthesized voice.
- **🧠 Aman Sharma Persona**: The AI believes it is a human engineer, strictly avoiding "As an AI" cliches.
- **⚡ High-Speed Responses**: Powered by **Google Gemini 2.5 Flash** for near-instant replies.
- **📅 Context Aware**: Knows the real-time date and time.
- **🛡️ Robust Error Handling**: Automatically switches models and handles network issues gracefully.
- **🎨 Premium UI**: A clean, modern dark-themed interface with glassmorphism effects.

---

## 🛠️ Technology Stack

- **Frontend**: 
  - HTML5, CSS3 (Custom Design)
  - Vanilla JavaScript
  - Web Speech API (Speech Recognition & Synthesis)
- **Backend**: 
  - Python 3.x
  - FastAPI (High-performance web framework)
  - Google GenAI SDK (`google-genai`)
  - Uvicorn (ASGI Server)

---

## 🏃‍♂️ How to Run Locally

### 1. Prerequisites
- Python 3.9 or higher installed.
- A Google Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/)).

### 2. Backward Setup (Server)
Navigate to the backend folder and install dependencies:
```bash
cd voice-me/backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
```ini
GEMINI_API_KEY=your_api_key_here
```

Start the server (Runs on Port 8001):
```bash
python -m uvicorn backend.main:app --port 8001 --reload
```

### 3. Frontend Setup (Client)
Simply open the `index.html` file in your browser:
- Go to `voice-me/frontend`
- Double-click `index.html` OR use Live Server in VS Code.

---

## 💡 Usage Guide

1. **Click the Microphone Button**: The bot will start listening.
2. **Ask a Question**: Try asking:
   - *"Tell me about yourself."*
   - *"What is your superpower?"*
   - *"What day is it today?"*
3. **Listen**: The bot will answer verbally and display the text on screen.

---

## 🔧 Troubleshooting

- **"Thinking..." forever?** 
  - Ensure the backend server is running on **Port 8001**.
  - Refresh the page to reconnect.
- **"Sorry, something went wrong?"**
  - Check your internet connection.
  - Verify your API Key in `backend/.env`.

---

**Built with ❤️ by Aman Sharma**