import os
from dotenv import load_dotenv

# Explicitly search and load your local .env configuration file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Active system validation alert
if not GROQ_API_KEY:
    print("\n[CRITICAL SYSTEM WARNING]: GROQ_API_KEY was not found inside your .env file!")
    print("-> Please double-check that your file is named exactly '.env' (with a dot at the start).")
    print("-> Ensure it contains: GROQ_API_KEY=your_actual_groq_key_here\n")
