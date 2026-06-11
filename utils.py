from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# ── Get API key ───────────────────────────────────────────────
def get_api_key():
    # First try Streamlit secrets (Streamlit Cloud)
    try:
        import streamlit as st
        key = st.secrets.get("GROQ_API_KEY", None)
        if key:
            return key
    except Exception:
        pass

    # Fall back to .env file (local development)
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key

    raise ValueError(
        "GROQ_API_KEY not found. Add it to .env locally "
        "or to Streamlit secrets on cloud."
    )

api_key = get_api_key()

# ── Groq Client ───────────────────────────────────────────────
client = Groq(api_key=api_key)


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to Groq and returns the response.
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