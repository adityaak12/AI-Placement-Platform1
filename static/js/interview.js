document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.querySelector('.chat-container');
    const answerInput = document.getElementById('interview-answer-input');
    const wordCountSpan = document.getElementById('word-count-span');
    const speechBtn = document.getElementById('speech-mic-btn');

    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    if (answerInput && wordCountSpan) {
        answerInput.addEventListener('input', function () {
            const words = this.value.trim().split(/\s+/).filter(Boolean);
            wordCountSpan.textContent = `${words.length} words`;
        });
    }

    // Web Speech API for voice-based interview practice (SRS Future Scope / Feature)
    if (speechBtn && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        let isListening = false;

        speechBtn.addEventListener('click', function () {
            if (!isListening) {
                recognition.start();
                speechBtn.classList.add('btn-danger');
                speechBtn.innerHTML = '<i class="bi bi-mic-fill me-1"></i> Listening...';
                isListening = true;
            } else {
                recognition.stop();
                speechBtn.classList.remove('btn-danger');
                speechBtn.innerHTML = '<i class="bi bi-mic me-1"></i> Speak Answer';
                isListening = false;
            }
        });

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            if (answerInput) {
                answerInput.value = (answerInput.value ? answerInput.value + ' ' : '') + transcript;
                answerInput.dispatchEvent(new Event('input'));
            }
            speechBtn.classList.remove('btn-danger');
            speechBtn.innerHTML = '<i class="bi bi-mic me-1"></i> Speak Answer';
            isListening = false;
        };

        recognition.onerror = function () {
            speechBtn.classList.remove('btn-danger');
            speechBtn.innerHTML = '<i class="bi bi-mic me-1"></i> Speak Answer';
            isListening = false;
        };
    } else if (speechBtn) {
        speechBtn.style.display = 'none';
    }
});
