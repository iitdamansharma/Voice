const micButton = document.getElementById('micButton');
const statusDiv = document.getElementById('status');
const questionText = document.getElementById('questionText');
const answerText = document.getElementById('answerText');

// Check for API support
if (!('webkitSpeechRecognition' in window)) {
    alert('Web Speech API is not supported in this browser. Please use Google Chrome.');
}

const recognition = new webkitSpeechRecognition();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = 'en-US'; // or en-IN

let isListening = false;

micButton.addEventListener('click', toggleListening);

function toggleListening() {
    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
        updateUIState('listening');
    }
}

recognition.onstart = function () {
    isListening = true;
    updateUIState('listening');
};

recognition.onend = function () {
    isListening = false;
    // Don't reset to ready immediately if we are processing, wait for result or error
    if (statusDiv.textContent === 'Listening...') {
        updateUIState('ready');
    }
};

recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    displayQuestion(transcript);
    processQuestion(transcript);
};

recognition.onerror = function (event) {
    console.error('Speech recognition error', event.error);
    statusDiv.textContent = 'Error: ' + event.error;
    isListening = false;
    updateUIState('ready');
};


function updateUIState(state) {
    const container = document.querySelector('.mic-container');
    if (state === 'listening') {
        container.classList.add('listening');
        statusDiv.textContent = 'Listening...';
        statusDiv.style.color = '#f87171';
        statusDiv.style.borderColor = 'rgba(239, 68, 68, 0.3)';
    } else if (state === 'processing') {
        container.classList.remove('listening');
        statusDiv.textContent = 'Thinking...';
        statusDiv.style.color = '#fbbf24';
        statusDiv.style.borderColor = 'rgba(251, 191, 36, 0.3)';
    } else if (state === 'speaking') {
        container.classList.remove('listening');
        statusDiv.textContent = 'Speaking...';
        statusDiv.style.color = '#34d399';
        statusDiv.style.borderColor = 'rgba(52, 211, 153, 0.3)';
    } else {
        container.classList.remove('listening');
        statusDiv.textContent = 'Ready to Listen';
        statusDiv.style.color = '#cbd5e1';
        statusDiv.style.borderColor = 'rgba(255, 255, 255, 0.1)';
    }
}

function displayQuestion(text) {
    questionText.textContent = text;
    questionText.classList.remove('placeholder-text');
}

function displayAnswer(text) {
    answerText.textContent = text;
    answerText.classList.remove('placeholder-text');
}

async function processQuestion(question) {
    updateUIState('processing');

    try {
        const response = await fetch('http://localhost:8001/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const data = await response.json();
        const answer = data.answer;

        displayAnswer(answer);
        speakAnswer(answer);

    } catch (error) {
        console.error('Error fetching answer:', error);
        answerText.textContent = 'Sorry, something went wrong. Please check the backend connection.';
        statusDiv.textContent = 'Error';
        setTimeout(() => updateUIState('ready'), 3000);
    }
}

function speakAnswer(text) {
    if ('speechSynthesis' in window) {
        updateUIState('speaking');

        // Cancel any current speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);

        // Improve voice selection
        const voices = window.speechSynthesis.getVoices();
        // Try to find a male voice like "Google UK English Male" or similar if possible, otherwise default
        const preferredVoice = voices.find(voice => voice.name.includes('Google US English') || voice.name.includes('Male'));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        utterance.rate = 1;
        utterance.pitch = 1;

        utterance.onend = function () {
            updateUIState('ready');
        };

        window.speechSynthesis.speak(utterance);
    } else {
        alert("Text-to-Speech not supported in this browser.");
        updateUIState('ready');
    }
}
