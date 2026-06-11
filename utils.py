from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

# ── API Key Setup ─────────────────────────────────────────────
# On Streamlit Cloud → reads from secrets.toml
# On your local laptop → reads from .env file
try:
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

# ── Groq Client ───────────────────────────────────────────────
client = Groq(api_key=api_key)


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to Groq (Llama 3.3 70B) and returns the response.
    All 6 agents in agents.py call this function.
    Works both locally and on Streamlit Cloud.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"[ERROR] Could not get response from Groq: {str(e)}"