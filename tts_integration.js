class PythonTTSClient {
    constructor(serverUrl = 'http://localhost:5000') {
        this.serverUrl = serverUrl;
        this.isAvailable = false;
        this.checkAvailability();
    }

    async checkAvailability() {
        try {
            const response = await fetch(`${this.serverUrl}/status`);
            this.isAvailable = response.ok;
            return this.isAvailable;
        } catch (error) {
            this.isAvailable = false;
            return false;
        }
    }

    async speak(text, options = {}) {
        if (!this.isAvailable) {
            console.warn('Python TTS server is not available');
            return false;
        }

        try {
            const response = await fetch(`${this.serverUrl}/speak`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    method: options.method || 'pyttsx3',
                    params: {
                        volume: options.volume || 0.8,
                        rate: options.rate || 150,
                        voice_id: options.voiceId,
                        lang: options.lang || 'en',
                        slow: options.slow || false
                    }
                })
            });

            return response.ok;
        } catch (error) {
            console.error('Failed to speak:', error);
            return false;
        }
    }

    async stop() {
        try {
            const response = await fetch(`${this.serverUrl}/stop`, {
                method: 'POST'
            });
            return response.ok;
        } catch (error) {
            console.error('Failed to stop:', error);
            return false;
        }
    }

    async getVoices() {
        try {
            const response = await fetch(`${this.serverUrl}/voices`);
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            console.error('Failed to get voices:', error);
            return null;
        }
    }

    async getStatus() {
        try {
            const response = await fetch(`${this.serverUrl}/status`);
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            return null;
        }
    }
}

// Example integration code for index.html
function integrateWithPythonTTS() {
    const ttsClient = new PythonTTSClient();
    
    // Add this to your existing speakText function
    async function speakTextWithPython(text) {
        const usePythonTTS = document.getElementById('usePythonTTS')?.checked;
        
        if (usePythonTTS && ttsClient.isAvailable) {
            // Use Python TTS
            const success = await ttsClient.speak(text, {
                method: 'gtts', // or 'pyttsx3'
                volume: parseFloat(volumeSlider.value),
                rate: parseFloat(rateSlider.value) * 100 + 50, // Convert to pyttsx3 scale
                lang: 'en'
            });
            
            if (!success) {
                // Fallback to browser TTS
                speakText(text);
            }
        } else {
            // Use browser TTS
            speakText(text);
        }
    }
    
    // Check Python TTS availability periodically
    setInterval(async () => {
        const available = await ttsClient.checkAvailability();
        const indicator = document.getElementById('pythonTTSStatus');
        if (indicator) {
            indicator.style.display = available ? 'inline' : 'none';
        }
    }, 5000);
    
    return ttsClient;
} 