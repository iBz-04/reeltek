import requests
import time

def test_tts_server():
    base_url = "http://localhost:5000"
    
    print("Testing Server...")
    
    # Test 1: Check status
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            print("running")
            print(f"  Status: {response.json()}")
        else:
            print("Server not responding")
            return
    except:
        print("Could not connect to server. Make sure tts_server.py is running.")
        return
    
    # Test 2: Get voices
    response = requests.get(f"{base_url}/voices")
    if response.status_code == 200:
        voices = response.json()
        print(f"✓ Found {len(voices['pyttsx3_voices'])} pyttsx3 voices")
        print(f"✓ Found {len(voices['gtts_languages'])} gTTS languages")
    
    # Test 3: Speak with pyttsx3
    print("\nTesting pyttsx3...")
    response = requests.post(f"{base_url}/speak", json={
        "text": "Hello from pyttsx3 text to speech engine",
        "method": "pyttsx3",
        "params": {"volume": 0.8, "rate": 150}
    })
    if response.status_code == 200:
        print("✓ pyttsx3 speech queued")
        time.sleep(3)
    
    # Test 4: Speak with gTTS
    print("\nTesting gTTS...")
    response = requests.post(f"{base_url}/speak", json={
        "text": "Hello from Google text to speech",
        "method": "gtts",
        "params": {"volume": 0.8, "lang": "en"}
    })
    if response.status_code == 200:
        print("✓ gTTS speech queued")
        time.sleep(3)
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_tts_server() 