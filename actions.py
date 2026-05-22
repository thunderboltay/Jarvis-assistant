import os
import time
import datetime
import webbrowser
import pyautogui
# Connect directly to your custom components
from ai import ask_ai
from voice import speak
import ctypes # Native operating system library connector

# Import specialized Windows Runtime Notification Management modular namespaces
try:
    import winrt.windows.ui.notifications.management as winrt_management
    import winrt.windows.ui.notifications as winrt_notifications
except ImportError:
    pass

# Global persistent tracking flag for WinRT alerts
last_processed_notification_id = 0

# ---------------- WEBSITES ----------------
def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://youtube.com")

def open_instagram():
    speak("Opening Instagram")
    webbrowser.open("https://instagram.com")

def open_google():
    speak("Opening Google")
    webbrowser.open("https://google.com")

def open_aynix():
    speak("Opening aynix")
    webbrowser.open("https://aynixglobal.com")

# ---------------- SEARCH ----------------
def search_google(query):
    search = query.replace("search", "").strip()
    if search:
        speak(f"Searching for {search}")
        url = f"google.com{search}"
        webbrowser.open(url)
    else:
        speak("What would you like me to search for, sir?")

# ---------------- APPS ----------------
def open_discord():
    speak("Opening Discord")
    # Developer fix: Uses the reliable environment shortcut macro path
    os.system('start "" "%localappdata%\\Discord\\Update.exe" --processStart Discord.exe')

def open_spotify():
    speak("Opening Spotify")
    webbrowser.open("spotify://")

def open_vscode():
    speak("Opening Visual Studio Code")
    os.system("code")

# ---------------- SPOTIFY AUTOMATION ----------------
def play_song(query):
    song = query.replace("play", "").strip()
    if not song:
        speak("What song should I play, sir?")
        return
        
    speak(f"Playing {song}")
    webbrowser.open("spotify://")
    time.sleep(5) # Wait for application load
    pyautogui.hotkey('ctrl', 'l') # Focus search bar
    time.sleep(0.5)
    pyautogui.write(song, interval=0.03)
    pyautogui.press('enter')

# ---------------- TIME ----------------
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

# ---------------- LOCK PC ----------------
def lock_pc():
    speak("Locking your PC now, sir.")
    try:
        # Calls the core Windows User32 library directly to mimic Win + L exactly
        ctypes.windll.user32.LockWorkStation()
    except Exception as e:
        print(f"[Windows 11 Lock API Failed]: {e}")
        # Subprocess shell execution fallback if system execution handles are restricted
        os.system("rundll32.exe user32.dll,LockWorkStation")

# ---------------- ESSAY WRITER ----------------
def write_essay(topic):
    topic_clean = topic.strip()
    if not topic_clean:
        speak("Please specify a topic for the essay, sir.")
        return
        
    speak(f"Writing your essay on {topic_clean}")
    essay = ask_ai(f"Write a detailed essay about {topic_clean}")
    os.system("start winword")
    time.sleep(6) # Generous safety window for MS Word initialization
    pyautogui.write(essay, interval=0.01)
    speak("Essay completed")

# ---------------- CODE WRITER ----------------
def write_code(prompt):
    prompt_clean = prompt.strip()
    if not prompt_clean:
        speak("Please specify what code I should write, sir.")
        return
        
    speak("Generating code")
    code = ask_ai(f"Only return clean, valid code. Absolutely no explanations, markdown formatting, backticks, or text. {prompt_clean}")
    os.system("code")
    time.sleep(5) # Let VS Code window settle and gain keyboard focus
    pyautogui.write(code, interval=0.01)
    speak("Code written")

# ---------------- DISCORD AUTOMATION ----------------
def discord_chat_writer(message_prompt):
    if not message_prompt.strip():
        speak("What would you like me to say in the chat, sir?")
        return
        
    speak("Generating response and accessing Discord")
    chat_content = ask_ai(f"Write a brief, casual chat message for Discord based on this instruction: {message_prompt}")
    os.system('start "" "%localappdata%\\Discord\\Update.exe" --processStart Discord.exe')
    time.sleep(7)
    
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(0.5)
    pyautogui.write(chat_content, interval=0.01)
    pyautogui.press('enter')
    speak("Message transmitted successfully, sir.")

# ---------------- NOTIFICATION SYSTEM ----------------
# FIX: Added the missing function definition header and indented the logic below it
def check_discord_notifications():
    global last_processed_notification_id
    try:
        # Access using the updated module namespace layouts cleanly
        listener = winrt_management.UserNotificationListener.get_current()
        toasts = listener.get_notifications(winrt_notifications.NotificationKinds.TOAST)
        
        if not toasts:
            return False
            
        for notification in toasts:
            if hasattr(notification, "app_info"):
                app_name = notification.app_info.display_info.display_name.lower()
                
                # Check if the notification belongs to Discord
                if "discord" in app_name:
                    current_id = notification.id
                    
                    # Verify if this is a brand new unhandled notification
                    if current_id != last_processed_notification_id:
                        last_processed_notification_id = current_id
                        return True
        return False
    except Exception:
        return False
