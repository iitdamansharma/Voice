# 🎙️ VoiceMe - AI Interview Voice Agent (Improved)

**VoiceMe** is an interactive voice-based AI agent designed to simulate a real human conversation. It adopts the persona of **Aman Sharma**, a passionate software engineer, capable of answering interview questions with a distinct personality, resilience, and professional tone.

## 🚀 What's New in Version 2.0

This improved version addresses critical feedback about creating a "more seamless experience" with comprehensive enhancements across all aspects of the application.

### ✨ Major Improvements

#### **1. Enhanced User Experience**
- ✅ **Intelligent Error Recovery**: Automatic retry logic with exponential backoff
- ✅ **Clear Status Indicators**: Real-time feedback with visual cues for all states
- ✅ **Conversation History**: Track and review past Q&A sessions
- ✅ **Text Input Fallback**: Type questions if voice recognition fails
- ✅ **Keyboard Shortcuts**: Power user controls (Space, Enter, Esc)
- ✅ **Browser Compatibility Warning**: Graceful degradation for unsupported browsers
- ✅ **Responsive Design**: Optimized for mobile, tablet, and desktop

#### **2. Performance Optimizations**
- ⚡ **Request Caching**: Smart caching to reduce API calls
- ⚡ **Concurrent Processing**: Optimized async/await patterns
- ⚡ **Loading States**: Visual feedback during processing
- ⚡ **Timeout Handling**: Proper timeout management to prevent hanging
- ⚡ **Preloaded Voices**: Faster TTS initialization

#### **3. Robust Error Handling**
- 🛡️ **Multi-Level Fallback**: Gemini → OpenAI → Groq with automatic switching
- 🛡️ **Detailed Error Messages**: User-friendly error descriptions
- 🛡️ **Network Error Recovery**: Automatic retry with exponential backoff
- 🛡️ **Input Validation**: Server-side and client-side validation
- 🛡️ **Comprehensive Logging**: Detailed logging for debugging

#### **4. Code Quality Improvements**
- 🔧 **Modular Architecture**: Clean separation of concerns
- 🔧 **Type Safety**: Pydantic models for validation
- 🔧 **Configuration Management**: Centralized configuration
- 🔧 **Error Handling**: Proper exception handling throughout
- 🔧 **Documentation**: Inline comments and docstrings
- 🔧 **Best Practices**: Following Python and JavaScript best practices

#### **5. New Features**
- 🎯 **Retry Button**: Easily retry failed requests
- 🎯 **Voice Selection**: Choose from available TTS voices
- 🎯 **Speech Controls**: Adjustable rate, pitch, and volume
- 🎯 **Conversation History**: Scrollable history with timestamps
- 🎯 **Health Check Endpoint**: Monitor API service availability
- 🎯 **API Documentation**: Automatic OpenAPI/Swagger docs

---

## 📋 Features

- **🎤 Voice-to-Voice Interaction**: Speak naturally to the bot, and it replies with a synthesized voice
- **🤖 Aman Sharma Persona**: The AI believes it is a human engineer, strictly avoiding "As an AI" clichés
- **⚡ High-Speed Responses**: Powered by Google Gemini 2.5 Flash with automatic fallbacks
- **📅 Context Aware**: Knows the real-time date and time
- **🛡️ Robust Error Handling**: Automatically switches models and handles network issues gracefully
- **🎨 Premium UI**: Clean, modern dark-themed interface with glassmorphism effects
- **⌨️ Keyboard Shortcuts**: Quick access to common functions
- **📱 Responsive Design**: Works seamlessly on all devices

---

## 🛠️ Technology Stack

### **Frontend**
- **HTML5**: Semantic markup structure
- **CSS3**: Custom design with animations and transitions
- **Vanilla JavaScript**: No framework dependencies
- **Web Speech API**: Speech Recognition & Synthesis

### **Backend**
- **Python 3.9+**: Modern Python with type hints
- **FastAPI**: High-performance async web framework
- **Pydantic**: Data validation and settings management
- **Google GenAI SDK**: Primary AI service
- **OpenAI SDK**: Backup AI service
- **Groq SDK**: Fallback AI service
- **Uvicorn**: ASGI server

---

## 🚀 Quick Start

### **Option 1: Deployed Version (Easiest)**
Simply visit the deployed application and start talking!

### **Option 2: Run Locally**

#### **Prerequisites**
- Python 3.9 or higher
- npm or node (optional, for some development tools)
- Google Gemini API Key (get it from [Google AI Studio](https://aistudio.google.com/))

#### **Backend Setup**

1. **Navigate to the backend directory:**
```bash
cd Voice/backend
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create a `.env` file:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional
GROQ_API_KEY=your_groq_api_key_here      # Optional
```

5. **Start the server:**
```bash
python main-improved.py
```
The server will run on `http://localhost:8001`

#### **Frontend Setup**

Simply open `index-improved.html` in your browser:

1. **Navigate to the frontend directory:**
```bash
cd Voice/frontend
```

2. **Open the HTML file:**
   - Double-click `index-improved.html`, OR
   - Use Live Server in VS Code, OR
   - Use Python's built-in server:
     ```bash
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

---

## 📖 Usage Guide

### **Voice Interaction**
1. **Click the Microphone Button** or press **Space** to start listening
2. **Ask a Question** (examples below)
3. **Listen** to the AI's verbal response
4. **View** the conversation on screen

### **Text Input Fallback**
1. **Type your question** in the text input field
2. **Press Enter** or click **Send**
3. **Receive** the AI's response

### **Sample Questions to Try**
- *"Tell me about yourself."*
- *"What's your #1 superpower?"*
- *"What are the top 3 areas you'd like to grow in?"*
- *"What misconception do your coworkers have about you?"*
- *"How do you push your boundaries and limits?"*
- *"What day is it today?"*

### **Keyboard Shortcuts**
- **Space**: Toggle microphone (when not typing)
- **Enter**: Send text input
- **Esc**: Stop speaking

---

## 🏗️ Project Structure

```
Voice/
├── backend/
│   ├── main-improved.py          # Improved FastAPI backend
│   ├── main.py                   # Original backend (for reference)
│   └── .env                      # API keys (not in git)
├── frontend/
│   ├── index-improved.html       # Improved frontend
│   ├── style-improved.css        # Enhanced styles
│   ├── app-improved.js           # Improved JavaScript
│   ├── index.html                # Original frontend (reference)
│   ├── style.css                 # Original styles (reference)
│   └── app.js                    # Original JavaScript (reference)
├── README.md                     # Original README
└── README-IMPROVED.md            # This file
```

---

## 🔧 Configuration

### **Backend Configuration (Config class)**
```python
class Config:
    GEMINI_MODEL = "gemini-2.5-flash"
    OPENAI_MODEL = "gpt-4o-mini"
    GROQ_MODEL = "llama-3.3-70b-versatile"
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    REQUEST_TIMEOUT = 30
    MAX_TOKENS = 200
    TEMPERATURE = 0.7
```

### **Frontend Configuration (CONFIG object)**
```javascript
const CONFIG = {
    backendUrl: '/ask',  // Auto-detects localhost vs production
    speechSettings: {
        lang: 'en-US',
        rate: 1.0,
        pitch: 1.0,
        volume: 1.0
    },
    uiSettings: {
        autoScroll: true,
        showTimestamps: true,
        maxHistoryItems: 10
    }
};
```

---

## 🐛 Troubleshooting

### **"Thinking..." forever?**
- ✅ Ensure the backend server is running on **Port 8001**
- ✅ Check the browser console for errors
- ✅ Verify API keys in `backend/.env`
- ✅ Try the text input fallback

### **"Sorry, something went wrong?"**
- ✅ Check your internet connection
- ✅ Verify your API key is valid
- ✅ Check the backend logs for specific errors
- ✅ Try clicking the "Retry" button

### **Microphone not working?**
- ✅ Allow microphone permissions in your browser
- ✅ Use Google Chrome or Microsoft Edge (best support)
- ✅ Check if another app is using the microphone
- ✅ Try the text input fallback

### **Backend connection issues?**
- ✅ Verify the backend is running: `curl http://localhost:8001/health`
- ✅ Check if firewall is blocking port 8001
- ✅ Review backend logs for errors
- ✅ Ensure all dependencies are installed

---

## 📊 API Endpoints

### **GET /** - Root endpoint
Returns API information and available endpoints.

### **GET /health** - Health check
Returns service status and availability of AI services.

### **POST /ask** - Ask a question
**Request Body:**
```json
{
  "question": "What's your superpower?"
}
```

**Response:**
```json
{
  "answer": "I learn rapidly and break complex problems into clear first principles...",
  "model_used": "gemini",
  "response_time": 1.23,
  "timestamp": "2024-01-15T10:30:00"
}
```

### **GET /docs** - API documentation
Interactive OpenAPI/Swagger documentation.

---

## 🔒 Security Considerations

- ✅ **API Keys**: Never commit API keys to git
- ✅ **CORS**: Configure appropriately for production
- ✅ **Input Validation**: All inputs are validated server-side
- ✅ **Rate Limiting**: Implement rate limiting in production
- ✅ **Error Messages**: Don't expose sensitive information in errors

---

## 🚀 Deployment

### **Frontend Deployment (Vercel/Netlify)**
1. Upload `frontend/` directory
2. Configure build settings if needed
3. Deploy!

### **Backend Deployment (Render/Heroku)**
1. Create a new web service
2. Set environment variables (API keys)
3. Deploy `backend/main-improved.py`
4. Update frontend `CONFIG.backendUrl` if needed

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🙏 Acknowledgments

- **100x Team** for the assessment opportunity
- **Google AI** for the Gemini API
- **OpenAI** for the GPT API
- **Groq** for the fast inference API
- The open-source community for amazing tools

---

## 📧 Contact

Built with ❤️ by **Aman Sharma**

For questions or feedback, please reach out through the assessment channels.

---

## 🎯 Assessment Improvements Summary

This improved version directly addresses the assessment feedback by creating a **more seamless experience** through:

1. **Eliminated Manual Configuration**: Users no longer need to manually enter API keys
2. **Automatic Error Recovery**: Graceful handling of all error scenarios
3. **Clear User Feedback**: Real-time status updates and error messages
4. **Multiple Input Methods**: Voice and text input with seamless fallback
5. **Browser Compatibility**: Works across different browsers with graceful degradation
6. **Professional UI/UX**: Clean, intuitive interface with visual feedback
7. **Robust Backend**: Reliable API with proper error handling and logging
8. **Comprehensive Documentation**: Clear setup and usage instructions

**The result is a production-ready application that provides a smooth, professional user experience out of the box.** ✨