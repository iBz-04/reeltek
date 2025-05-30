# Speech Synthesis for ReelTek Vision System

This document explains how to use the speech synthesis features added to the ReelTek Vision System.

## Overview

The system now includes two speech synthesis options:

1. **Browser-based Speech Synthesis** (Built-in, no setup required)
2. **Python TTS Server** (Optional, better voice quality)

## Browser-based Speech Synthesis

### Features
- Works immediately in modern browsers
- No additional setup required
- Multiple voice options based on your system
- Adjustable volume and speech rate
- Automatic queue management for smooth playback

### How to Use
1. Open `index.html` in your browser
2. Start the camera and vision analysis as usual
3. Check the "Enable Speech Output" checkbox
4. The system will speak the AI's descriptions aloud
5. Adjust voice, volume, and speed using the controls

### Browser Compatibility
- Chrome/Edge: Excellent support with many voices
- Firefox: Good support with system voices
- Safari: Basic support with limited voices

## Python TTS Server (Optional)

### Features
- Higher quality voices
- More voice options
- Support for multiple languages
- Two TTS engines:
  - **pyttsx3**: Fast, offline, system voices
  - **gTTS (Google TTS)**: High quality, requires internet

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements_tts.txt
```

2. Run the TTS server:
```bash
python tts_server.py
```

3. The server will start on `http://localhost:5000`

### API Endpoints

- `POST /speak` - Convert text to speech
  ```json
  {
    "text": "Hello world",
    "method": "gtts",
    "params": {
      "volume": 0.8,
      "rate": 150,
      "lang": "en"
    }
  }
  ```

- `GET /voices` - List available voices
- `POST /stop` - Stop current speech
- `GET /status` - Check server status

### Integration with ReelTek

To use Python TTS instead of browser TTS:

1. Include `tts_integration.js` in your HTML:
```html
<script src="tts_integration.js"></script>
```

2. The system will automatically detect if the Python TTS server is running
3. You can add a toggle to switch between browser and Python TTS

## Troubleshooting

### Browser TTS Issues
- **No voices available**: Check browser permissions for speech
- **Speech cuts off**: Reduce analysis frequency in settings
- **Wrong voice**: Try different browsers for more voice options

### Python TTS Issues
- **Server won't start**: Check if port 5000 is available
- **No sound**: Ensure system audio is working
- **pyttsx3 errors**: Install system speech engines (Windows: SAPI5, Linux: espeak)
- **gTTS errors**: Check internet connection

## Performance Tips

1. **For real-time analysis**: Use shorter speech snippets
2. **Reduce queue buildup**: Lower the analysis frequency
3. **Better performance**: Use pyttsx3 over gTTS for faster response
4. **Smooth playback**: The system automatically manages speech queues

## Advanced Configuration

### Custom Voice Settings
Modify the speech parameters in the code:
```javascript
utterance.pitch = 1.2;  // Higher pitch
utterance.rate = 0.9;   // Slower speech
```

### Language Support
For multilingual support with gTTS:
```python
tts = gTTS(text=text, lang='es')  # Spanish
tts = gTTS(text=text, lang='fr')  # French
```

## Future Enhancements

Potential improvements you could add:
- Save speech to audio files
- Custom voice models
- Emotion-based voice modulation
- Background music/sound effects
- Voice commands for control 