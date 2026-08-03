// Voice input for answer textareas, using the browser's built-in
// Web Speech API. No server-side processing — everything happens
// in the browser, so this works the same locally and on Render.
(function () {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    document.querySelectorAll('.mic-btn').forEach(function (btn) {
        if (!SpeechRecognition) {
            btn.disabled = true;
            btn.classList.add('mic-unsupported');
            btn.title = 'Voice input isn\'t supported in this browser — try Chrome or Edge';
            return;
        }

        const targetId = btn.getAttribute('data-target');
        const field = document.getElementById(targetId);
        if (!field) return;

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;

        let listening = false;

        btn.addEventListener('click', function () {
            if (listening) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (e) {
                    // start() throws if called while already starting; ignore
                }
            }
        });

        recognition.onstart = function () {
            listening = true;
            btn.classList.add('mic-recording');
            btn.textContent = '⏹';
            btn.title = 'Stop recording';
        };

        recognition.onend = function () {
            listening = false;
            btn.classList.remove('mic-recording');
            btn.textContent = '🎤';
            btn.title = 'Start voice input';
        };

        recognition.onerror = function (event) {
            listening = false;
            btn.classList.remove('mic-recording');
            btn.textContent = '🎤';
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
                alert('Microphone access was denied. Please allow microphone access in your browser to use voice input.');
            }
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            const existing = field.value.trim();
            field.value = existing ? existing + ' ' + transcript : transcript;
            field.dispatchEvent(new Event('input'));
        };
    });
})();