from actions import *
# Explicitly import your missing dependencies
from voice import speak
from ai import ask_ai

def execute_command(query):
    # Normalize input text
    query = query.lower().strip()
    
    # Ignore empty inputs to prevent accidental loops
    if not query:
        return

    # ---------------- WEBSITES ----------------
    if "open youtube" in query:
        open_youtube()
    elif "open instagram" in query:
        open_instagram()
    elif "open google" in query:
        open_google()
    elif "open aynix" in query:
        open_aynix()
        
    # ---------------- SEARCH ----------------
    elif query.startswith("search"):
        search_google(query)
        
    # ---------------- APPS ----------------
    elif "open discord" in query:
        open_discord()
    elif "open spotify" in query:
        open_spotify()
    elif "open vs code" in query or "open vscode" in query:
        open_vscode()
        
    # ---------------- MUSIC ----------------
    elif query.startswith("play"):
        play_song(query)
        
    # ---------------- TIME ----------------
    elif "time" in query:
        tell_time()
        
    # ---------------- LOCK PC ----------------
    elif "sleep mode" in query or "lock pc" in query:
        lock_pc()

    # ---------------- DISCORD AUTOMATION (PRIORITIZED) ----------------
    elif "tell discord to" in query or "message discord" in query:
        prompt = query.replace("tell discord to", "").replace("message discord", "").strip()
        discord_chat_writer(prompt)
        
    # ---------------- ESSAY ----------------
    elif "write essay on" in query:
        topic = query.replace("write essay on", "").strip()
        write_essay(topic)
        
    # ---------------- CODE ----------------
    elif "write code" in query:
        prompt = query.replace("write code", "").strip()
        write_code(prompt)
        
    # ---------------- AI CHAT FALLBACK ----------------
    else:
        # Passes text to main.py, which routes it cleanly to your UI log box
        response = ask_ai(query)
        speak(response)

