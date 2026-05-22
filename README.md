# JARVIS AI Assistant

An AI-powered personal assistant that can talk, respond, and perform system tasks using voice commands.

##  Features

- Voice activation using keyword: **"hey jarvis"**
- Voice-controlled commands for system automation
- Opens and controls apps like:
  - Spotify
  - Chrome
  - Instagram
- Music playback via Spotify using commands like:
  - `hey jarvis play <song name> on spotify app`
- Learns user preferences and stores them in `memory.json`
- Simple offline/online control system:
  - Activate: **"hey jarvis"**
  - Deactivate: **"go offline jarvis"**

---

##  Memory System

The assistant can learn basic user facts (preferences, likes, etc.) and store them locally in:


memory.json


This allows it to remember user details across sessions.

---

##  Installation

### 1. Download Project
Download or clone the repository and extract it.

### 2. Open in VS Code
Open the extracted folder in **Visual Studio Code**

### 3. Install Dependencies
Run the following command in terminal:

```bash
pip install winrt-runtime winrt windows.UI.Notifications winrt-windows.UI.Notifications.Management
pip install SpeechRecognition pyttsx3 pyautogui python-dotenv groq pyaudio pywin32 pygame edge-tts pydub imageio-ffmpeg
🔑 API Setup

This project uses Groq API.

Create a .env file in the root directory
Add your API key like this:
GROQ_API_KEY=PASTE_YOUR_API_KEY_HERE
▶️ How to Run

After installing dependencies:

python main.py

Then say:

"hey jarvis" → activate assistant
"go offline jarvis" → stop assistant
📌 Example Commands
hey jarvis open chrome
hey jarvis play starboy on spotify app
hey jarvis open instagram
⚠️ Notes
Requires internet for AI responses
Make sure microphone permissions are enabled
Works best on Windows systems
👨‍💻 Author

Ali Yahya

📄 License

This project is for educational and personal use.
      
