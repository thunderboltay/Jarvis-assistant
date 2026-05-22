# main.py
import random
import time
import threading
import tkinter as tk
from gui import JarvisGUI

import voice
from commands import execute_command
from actions import check_discord_notifications

app_gui = None
ACTIVE = False
WAKE_RESPONSES = ["Yes sir.", "I'm listening.", "How can I help?", "Ready sir."]

# ---------------- CORE INTERFACE WRAPPER FOR SPEECH ----------------
original_speak = voice.speak
def gui_speak_wrapper(text):
    if app_gui:
        app_gui.update_status("Speaking...", state="speaking")
        app_gui.append_log("Jarvis", text)
    original_speak(text)
    if app_gui:
        app_gui.update_status("Online & Standby", state="idle")

voice.speak = gui_speak_wrapper

# ---------------- BACKGROUND DISCORD NOTIFICATION WATCHER ----------------
def discord_alert_worker():
    already_alerted = False
    while True:
        notification_detected = check_discord_notifications()
        if notification_detected and not already_alerted:
            gui_speak_wrapper("Sir, you have received a new message notification on Discord.")
            already_alerted = True
        elif not notification_detected:
            already_alerted = False
        time.sleep(2)

# ---------------- CORE VOICE ASSISTANT PIPELINE THREAD ----------------
def voice_assistant_engine():
    global ACTIVE
    time.sleep(2) 
    gui_speak_wrapper("Jarvis online Ali Yahya sir!!.")
    
    while True:
        if app_gui:
            app_gui.update_status("Listening...", state="listening")
            
        query = voice.listen()
        if not query:
            if app_gui:
                app_gui.update_status("Online & Standby", state="idle")
            continue
            
        query = query.lower().strip()
        if app_gui:
            app_gui.append_log("You", query)
            
        if "hey jarvis" in query:
            ACTIVE = True
            query = query.replace("hey jarvis", "").strip()
            if not query:
                gui_speak_wrapper(random.choice(WAKE_RESPONSES)) 
                continue
            
        if ACTIVE:
            if "bye bye jarvis" in query or "bye bot" in query or "go offline" in query:
                gui_speak_wrapper("Going offline sir Ali. Goodbye! You are the best.")
                ACTIVE = False
                if app_gui:
                    app_gui.root.quit()
                break
                
            execute_command(query)

# ---------------- APPLICATION INITIALIZATION ROUTINE ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app_gui = JarvisGUI(root)
    app_gui.update_status("Online & Standby", state="idle")
    
    threading.Thread(target=voice_assistant_engine, daemon=True).start()
    threading.Thread(target=discord_alert_worker, daemon=True).start()
    
    root.mainloop()
