"""
LLM Client - Simple Groq Connection
====================================
One file. One client. All agents use this.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize Groq client (OpenAI-compatible)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Available models (for reference)
MODELS = {
    "fast": "llama-3.1-8b-instant",      # Fast responses, good for Q&A
    "smart": "llama-3.3-70b-versatile",  # Best reasoning, good for analysis
}
