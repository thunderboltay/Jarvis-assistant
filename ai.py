import json
import os
from groq import Groq
from config import GROQ_API_KEY

# Initialize the client immediately
client = Groq(api_key=GROQ_API_KEY)
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"user_name": "USER", "facts": {}}
    return {"user_name": "USER", "facts": {}}

def save_memory(memory_data):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_data, f, indent=4)
    except Exception as e:
        print(f"[Memory Save Error]: {e}")

def ask_ai(prompt):
    # Fallback to avoid catastrophic crashes if the API key failed to load
    if not GROQ_API_KEY:
        return "Sir SIR, sorry very much my API key is missing. Please check your config and dot env file."
        
    # 1. Load active memory matrix tracking parameters
    memory = load_memory()
    saved_facts = json.dumps(memory.get("facts", {}))
    
    # 2. Re-create your custom creator prompts injected with memory contexts
    SYSTEM_PROMPT = f"""
    You are JARVIS. You are  AI assistant.
    Be concise. Be smart. Keep replies short. Sound natural. Gen Z style. Use slangs.. 
    
    CURRENT USER MEMORIES AND PREFERENCES:
    {saved_facts}
    
    If user tells you a new fact about himself, a personal preference, or asks you to remember something, include the special tracking token '[UPDATE_MEMORY: key=value]' at the very end of your response text.
    Example: 'No cap sir, logged. [UPDATE_MEMORY: favorite_game=Valorant]'
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile"
        )
        reply = response.choices[0].message.content
        
        # 3. Intercept tracking keys and append straight to local memory files
        if "[UPDATE_MEMORY:" in reply:
            try:
                # Isolate matching token parameters
                parts = reply.split("[UPDATE_MEMORY:")
                token_content = parts[1].split("]")[0].strip()
                
                key, value = token_content.split("=", 1)
                memory["facts"][key.strip()] = value.strip()
                save_memory(memory)
                
                # Strip out tracking tag text so it doesn't leak into terminal windows or speakers
                reply = parts[0].strip()
            except Exception as parse_error:
                print(f"[Memory Parsing Warning]: {parse_error}")
                
        return reply
        
    except Exception as e:
        print(f"[Groq API Error]: {e}")
        return "I encountered an error connecting to my core neural network, sorry very much sir Ali !!."
