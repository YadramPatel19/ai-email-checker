from groq import Groq
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Connect to Groq using your API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to Groq (Llama 3 model) and returns the response.
    All 4 agents call this function.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # free, fast, very capable
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"[ERROR] Could not get response from Groq: {str(e)}"