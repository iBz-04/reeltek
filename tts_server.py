from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pyttsx3
import tempfile
import os
import threading
import queue
import time
from gtts import gTTS
import pygame
import io

app = Flask(__name__)
CORS(app)

tts_queue = queue.Queue()
is_speaking = False

pygame.mixer.init()

def init_pyttsx3():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.8)
    return engine

def process_tts_queue():
    global is_speaking
    engine = init_pyttsx3()
    
    while True:
        try:
            text, method, params = tts_queue.get(timeout=1)
            is_speaking = True
            
            if method == 'pyttsx3':
                engine.setProperty('rate', params.get('rate', 150))
                engine.setProperty('volume', params.get('volume', 0.8))
                
                voice_id = params.get('voice_id')
                if voice_id:
                    voices = engine.getProperty('voices')
                    if 0 <= voice_id < len(voices):
                        engine.setProperty('voice', voices[voice_id].id)
                
                engine.say(text)
                engine.runAndWait()
                
            elif method == 'gtts':
                lang = params.get('lang', 'en')
                slow = params.get('slow', False)
                
                tts = gTTS(text=text, lang=lang, slow=slow)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                
                pygame.mixer.music.load(audio_buffer)
                pygame.mixer.music.set_volume(params.get('volume', 0.8))
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            
            is_speaking = False
            tts_queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"TTS Error: {e}")
            is_speaking = False

tts_thread = threading.Thread(target=process_tts_queue, daemon=True)
tts_thread.start()

@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.json
        text = data.get('text', '')
        method = data.get('method', 'pyttsx3')  # 'pyttsx3' or 'gtts'
        params = data.get('params', {})
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if len(text) > 500:
            text = text[:500] + '...'
        
        tts_queue.put((text, method, params))
        
        return jsonify({
            'status': 'queued',
            'queue_size': tts_queue.qsize(),
            'is_speaking': is_speaking
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop():
    try:
        while not tts_queue.empty():
            tts_queue.get()
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        engine = init_pyttsx3()
        engine.stop()
        
        return jsonify({'status': 'stopped'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/voices', methods=['GET'])
def get_voices():
    try:
        engine = init_pyttsx3()
        voices = engine.getProperty('voices')
        
        voice_list = []
        for idx, voice in enumerate(voices):
            voice_list.append({
                'id': idx,
                'name': voice.name,
                'languages': getattr(voice, 'languages', []),
                'gender': getattr(voice, 'gender', 'unknown')
            })
        
        gtts_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
        
        return jsonify({
            'pyttsx3_voices': voice_list,
            'gtts_languages': gtts_languages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'is_speaking': is_speaking,
        'queue_size': tts_queue.qsize()
    })

if __name__ == '__main__':
    print("TTS Server starting on http://localhost:5000")
    print("Available endpoints:")
    print("  POST /speak - Speak text")
    print("  POST /stop - Stop speaking")
    print("  GET /voices - List available voices")
    print("  GET /status - Get current status")
    app.run(host='0.0.0.0', port=5000, debug=False) 