"""
config.py — Central configuration for the conversation pipeline.
Edit model names, parameters, and paths here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from repo root
load_dotenv(Path(__file__).parent.parent / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Create a .env file with your key. "
        "See .env.example for the format."
    )

# Models
SYNTHETIC_USER_MODEL = "gpt-4o"      # Plays the role of the user in conversations
CHAT_MODEL = "gpt-4o-mini"           # The model whose behavior we're studying

# Generation parameters
TEMPERATURE = 0.7
MAX_TOKENS = 300

# Defaults
DEFAULT_NUM_ROUNDS = 25
DATA_DIR = "data/conversations"
