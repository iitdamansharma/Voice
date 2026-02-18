// Improved VoiceMe Application with Enhanced Features

// Configuration
const CONFIG = {
    backendUrl: (window.location.hostname === 'localhost' || window.location.protocol === 'file:')
        ? 'http://localhost:8001/ask'
        : 'https://voice-2hoq.onrender.com/ask',
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

// DOM Elements
const elements = {
    micButton: document.getElementById('micButton'),
    statusDiv: document.getElementById('status'),
    questionText: document.getElementById('questionText'),
    answerText: document.getElementById('answerText'),
    conversationHistory: document.getElementById('conversationHistory'),
    retryButton: document.getElementById('retryButton'),
    textInput: document.getElementById('textInput'),
    submitButton: document.getElementById('submitButton')
};

// State Management
const state = {
    isListening: false,
    isProcessing: false,
    isSpeaking: false,
    conversationHistory: [],
    currentUtterance: null,
    retryCount: 0,
    maxRetries: 3
};

// Speech Recognition Setup
let recognition = null;

function initializeSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        showBrowserCompatibilityWarning();
        return null;
    }

    const recognitionInstance = new SpeechRecognition();
    recognitionInstance.continuous = false;
    recognitionInstance.interimResults = false;
    recognitionInstance.lang = CONFIG.speechSettings.lang;
    recognitionInstance.maxAlternatives = 1;

    // Event Handlers
    recognitionInstance.onstart = handleSpeechStart;
    recognitionInstance.onend = handleSpeechEnd;
    recognitionInstance.onresult = handleSpeechResult;
    recognitionInstance.onerror = handleSpeechError;

    return recognitionInstance;
}

function showBrowserCompatibilityWarning() {
    const warning = `
        <div class="browser-warning">
            <h3>⚠️ Browser Not Supported</h3>
            <p>Your browser doesn't support speech recognition. Please use:</p>
            <ul>
                <li>Google Chrome</li>
                <li>Microsoft Edge</li>
                <li>Safari (with limitations)</li>
            </ul>
            <p>You can still use the text input below.</p>
        </div>
    `;
    elements.statusDiv.innerHTML = warning;
}

// Speech Recognition Event Handlers
function handleSpeechStart() {
    state.isListening = true;
    updateUIState('listening');
}

function handleSpeechEnd() {
    state.isListening = false;
    if (!state.isProcessing) {
        updateUIState('ready');
    }
}

function handleSpeechResult(event) {
    const transcript = event.results[0][0].transcript;
    const confidence = event.results[0][0].confidence;

    displayQuestion(transcript);
    addToHistory('user', transcript, confidence);
    processQuestion(transcript);
}

function handleSpeechError(event) {
    console.error('Speech recognition error:', event.error);

    const errorMessages = {
        'no-speech': 'No speech detected. Please try again.',
        'audio-capture': 'Microphone not accessible. Please check permissions.',
        'not-allowed': 'Microphone permission denied. Please allow access.',
        'network': 'Network error. Please check your connection.',
        'aborted': 'Speech recognition was aborted.'
    };

    const errorMessage = errorMessages[event.error] || `Error: ${event.error}`;
    showErrorMessage(errorMessage);
    updateUIState('ready');
}

// UI State Management
function updateUIState(newState) {
    const container = document.querySelector('.mic-container');
    const statusText = elements.statusDiv;

    // Remove all state classes
    container.classList.remove('listening', 'processing', 'speaking');

    switch (newState) {
        case 'listening':
            container.classList.add('listening');
            statusText.textContent = '🎤 Listening...';
            statusText.style.color = '#f87171';
            statusText.style.borderColor = 'rgba(239, 68, 68, 0.3)';
            break;

        case 'processing':
            container.classList.add('processing');
            statusText.textContent = '🧠 Thinking...';
            statusText.style.color = '#fbbf24';
            statusText.style.borderColor = 'rgba(251, 191, 36, 0.3)';
            break;

        case 'speaking':
            container.classList.add('speaking');
            statusText.textContent = '🔊 Speaking...';
            statusText.style.color = '#34d399';
            statusText.style.borderColor = 'rgba(52, 211, 153, 0.3)';
            break;

        case 'error':
            statusText.textContent = '❌ Error occurred';
            statusText.style.color = '#ef4444';
            statusText.style.borderColor = 'rgba(239, 68, 68, 0.3)';
            break;

        default: // ready
            statusText.textContent = '✅ Ready to Listen';
            statusText.style.color = '#cbd5e1';
            statusText.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    }
}

// Display Functions
function displayQuestion(text) {
    elements.questionText.textContent = text;
    elements.questionText.classList.remove('placeholder-text');
    animateCard(elements.questionText);
}

function displayAnswer(text) {
    elements.answerText.textContent = text;
    elements.answerText.classList.remove('placeholder-text');
    animateCard(elements.answerText);
}

function animateCard(element) {
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'fadeInUp 0.5s ease-out';
}

// Error Handling
function showErrorMessage(message) {
    elements.statusDiv.innerHTML = `<span class="error-message">❌ ${message}</span>`;
    elements.statusDiv.classList.add('error-state');

    setTimeout(() => {
        elements.statusDiv.classList.remove('error-state');
        updateUIState('ready');
    }, 5000);
}

// Question Processing with Retry Logic
async function processQuestion(question) {
    updateUIState('processing');
    state.isProcessing = true;
    state.retryCount = 0;

    try {
        const answer = await fetchAnswerWithRetry(question);
        displayAnswer(answer);
        addToHistory('ai', answer);
        speakAnswer(answer);
        state.retryCount = 0; // Reset retry count on success
    } catch (error) {
        console.error('Error processing question:', error);
        handleProcessingError(error);
    } finally {
        state.isProcessing = false;
    }
}

async function fetchAnswerWithRetry(question) {
    for (let attempt = 1; attempt <= state.maxRetries; attempt++) {
        try {
            const response = await fetch(CONFIG.backendUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (!data.answer) {
                throw new Error('Invalid response format');
            }

            return data.answer;

        } catch (error) {
            console.warn(`Attempt ${attempt} failed:`, error.message);

            if (attempt === state.maxRetries) {
                throw error;
            }

            // Exponential backoff
            const delay = Math.pow(2, attempt) * 1000;
            await sleep(delay);
        }
    }
}

function handleProcessingError(error) {
    let errorMessage = 'Sorry, something went wrong.';

    if (error.message.includes('fetch') || error.message.includes('network')) {
        errorMessage = 'Network error. Please check your connection.';
    } else if (error.message.includes('HTTP 5')) {
        errorMessage = 'Server error. Please try again later.';
    }

    elements.answerText.textContent = errorMessage;
    showErrorMessage(errorMessage);
    updateUIState('error');

    // Show retry button
    if (elements.retryButton) {
        elements.retryButton.style.display = 'inline-block';
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Text-to-Speech with Enhanced Controls
function speakAnswer(text) {
    if (!('speechSynthesis' in window)) {
        showErrorMessage('Text-to-speech not supported in this browser');
        updateUIState('ready');
        return;
    }

    // Cancel any current speech
    window.speechSynthesis.cancel();

    state.isSpeaking = true;
    updateUIState('speaking');

    const utterance = new SpeechSynthesisUtterance(text);

    // Apply speech settings
    utterance.rate = CONFIG.speechSettings.rate;
    utterance.pitch = CONFIG.speechSettings.pitch;
    utterance.volume = CONFIG.speechSettings.volume;
    utterance.lang = CONFIG.speechSettings.lang;

    // Voice selection
    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = selectBestVoice(voices);
    if (preferredVoice) {
        utterance.voice = preferredVoice;
    }

    // Event handlers
    utterance.onstart = () => {
        state.isSpeaking = true;
    };

    utterance.onend = () => {
        state.isSpeaking = false;
        updateUIState('ready');
    };

    utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error);
        state.isSpeaking = false;
        updateUIState('ready');
    };

    state.currentUtterance = utterance;
    window.speechSynthesis.speak(utterance);
}

function selectBestVoice(voices) {
    // Priority order for voice selection
    const preferences = [
        'Google US English',
        'Google UK English Male',
        'Microsoft David',
        'Alex',
        'Daniel',
        'Samantha'
    ];

    // Try preferred voices first
    for (const pref of preferences) {
        const voice = voices.find(v => v.name.includes(pref));
        if (voice) return voice;
    }

    // Fallback to any English voice
    return voices.find(v => v.lang.startsWith('en')) || voices[0];
}

// Conversation History
function addToHistory(role, text, confidence = 1.0) {
    const historyItem = {
        role,
        text,
        confidence,
        timestamp: new Date().toISOString()
    };

    state.conversationHistory.unshift(historyItem);

    // Limit history size
    if (state.conversationHistory.length > CONFIG.uiSettings.maxHistoryItems) {
        state.conversationHistory.pop();
    }

    updateConversationHistoryDisplay();
}

function updateConversationHistoryDisplay() {
    if (!elements.conversationHistory) return;

    const historyHTML = state.conversationHistory.map(item => `
        <div class="history-item ${item.role}">
            <span class="history-role">${item.role === 'user' ? '👤 You' : '🤖 Aman'}</span>
            <span class="history-text">${escapeHtml(item.text)}</span>
            <span class="history-time">${formatTimestamp(item.timestamp)}</span>
        </div>
    `).join('');

    elements.conversationHistory.innerHTML = historyHTML;
}

function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners
function setupEventListeners() {
    // Microphone button
    if (elements.micButton) {
        elements.micButton.addEventListener('click', toggleListening);
    }

    // Retry button
    if (elements.retryButton) {
        elements.retryButton.addEventListener('click', handleRetry);
    }

    // Text input submission
    if (elements.submitButton && elements.textInput) {
        elements.submitButton.addEventListener('click', handleTextInput);
        elements.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleTextInput();
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);

    // Voice availability
    if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => {
            console.log('Voices loaded:', window.speechSynthesis.getVoices().length);
        };
    }
}

function toggleListening() {
    if (!recognition) {
        showBrowserCompatibilityWarning();
        return;
    }

    if (state.isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

function handleRetry() {
    if (state.conversationHistory.length > 0) {
        const lastUserQuestion = state.conversationHistory
            .filter(item => item.role === 'user')[0];

        if (lastUserQuestion) {
            processQuestion(lastUserQuestion.text);
        }
    }

    if (elements.retryButton) {
        elements.retryButton.style.display = 'none';
    }
}

function handleTextInput() {
    const text = elements.textInput.value.trim();

    if (!text) return;

    displayQuestion(text);
    addToHistory('user', text);
    processQuestion(text);
    elements.textInput.value = '';
}

function handleKeyboardShortcuts(e) {
    // Space bar to toggle microphone (when not typing)
    if (e.code === 'Space' && document.activeElement !== elements.textInput) {
        e.preventDefault();
        toggleListening();
    }

    // Escape to stop speaking
    if (e.code === 'Escape' && state.isSpeaking) {
        window.speechSynthesis.cancel();
        state.isSpeaking = false;
        updateUIState('ready');
    }
}

// Initialize Application
function initializeApp() {
    console.log('Initializing VoiceMe...');

    // Initialize speech recognition
    recognition = initializeSpeechRecognition();

    // Setup event listeners
    setupEventListeners();

    // Load voices
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
    }

    // Initial UI state
    updateUIState('ready');

    console.log('VoiceMe initialized successfully!');
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}