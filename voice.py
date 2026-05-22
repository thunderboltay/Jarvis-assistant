import os
import time  # Professional optimization for non-blocking wait threads
import asyncio
import speech_recognition as sr
import pyttsx3
from groq import Groq
import config

# CRITICAL FIX: Added missing library imports to prevent immediate NameErrors
import pygame
import edge_tts

# Initialize pygame mixer once for fast audio playback
pygame.mixer.init()

# Initialize Groq Cloud Client
groq_client = Groq(api_key=config.GROQ_API_KEY)
recognizer = sr.Recognizer()

def speak(text):
    print(f"Jarvis: {text}")
    # Premium human-sounding neural female voice options:
    # 'en-US-EmmaNeural' (Friendly, Natural)
    # 'en-US-AvaNeural' (Professional, Smooth)
    # 'en-GB-SoniaNeural' (Classy British Accent)
    VOICE = "en-US-EmmaNeural" 
    temp_file = "speech.mp3"
    
    try:
        # Stop any active audio before playing a new one
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        # Generate ultra-realistic speech stream
        communicate = edge_tts.Communicate(text, VOICE, rate="+10%")
        
        # FIX: Replaced non-existent save_sync with a safe async-to-sync runner block
        asyncio.run(communicate.save(temp_file))
        
        # Play the human voice file
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # PROFESSIONAL FIX: Added time.sleep to stop the infinite loop from maxing out CPU usage
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.music.unload()
        os.remove(temp_file)
        
    except Exception as e:
        print(f"[Premium Voice Error]: {e}")

def listen():
    with sr.Microphone() as source:
        # 1. Calibrate background room noise dynamically
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        # 2. Strict Threshold Gates (Prevents listening to fan/breathing noises)
        recognizer.energy_threshold = 250 # Ignore sounds quieter than this limit
        recognizer.dynamic_energy_threshold = False # Lock threshold so dead silence stays dead
        recognizer.pause_threshold = 0.6 # Cuts down waiting lag when you finish speaking
        recognizer.non_speaking_duration = 0.3
        
        print("\n[Listening (Groq Whisper Engaged)...]")
        
        try:
            # Capture the physical audio stream
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # 3. Size Filter: If the recorded audio snippet is too small, it's just a background click
            if len(audio.get_wav_data()) < 8000:
                return ""
                
            temp_filename = "temp_voice.wav"
            with open(temp_filename, "wb") as f:
                f.write(audio.get_wav_data())
                
            with open(temp_filename, "rb") as audio_file:
                transcription = groq_client.audio.transcriptions.create(
                    file=(temp_filename, audio_file.read()),
                    model="whisper-large-v3",
                    language="en",
                    response_format="text"
                )
                
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
            query = transcription.strip()
            if query:
                print(f"You: {query}")
                return query.lower().strip()
            return ""
            
        except Exception:
            if os.path.exists("temp_voice.wav"):
                os.remove("temp_voice.wav")
            return ""

