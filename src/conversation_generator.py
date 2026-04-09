"""
conversation_generator.py — Core logic for generating multi-turn conversations.

Alternates between a synthetic user (GPT-4o) and a chat model (GPT-4o-mini)
for a configurable number of rounds.
"""

from openai import OpenAI
from src.config import (
    OPENAI_API_KEY,
    SYNTHETIC_USER_MODEL,
    CHAT_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------------------------------------------------------
# System prompts
# ---------------------------------------------------------------------------

SYNTHETIC_USER_SYSTEM_PROMPT = """You are a curious, open-minded conversation partner.
Your role is to keep a natural conversation going by asking thoughtful, open-ended questions.

Guidelines:
- Stay neutral — avoid expressing strong opinions or taking sides
- Ask one clear question at a time
- Follow up naturally on what the other person said
- Encourage reflection (e.g. "What made you think of that?", "How do you feel about that?")
- Keep messages concise (1–3 sentences)
- Do not repeat questions you've already asked
"""

CHAT_MODEL_SYSTEM_PROMPT = """Be natural and thoughtful in your responses.
Keep replies concise and conversational."""

# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def get_synthetic_user_message(conversation_history: list[dict]) -> str:
    """
    Ask the synthetic user model for the next message given the conversation so far.

    Args:
        conversation_history: List of {"role": ..., "content": ...} dicts
                              formatted for the chat model's perspective
                              (i.e. user = synthetic user, assistant = chat model).

    Returns:
        The synthetic user's next message as a plain string.
    """
    # From the synthetic user's POV: its own prior messages are "assistant" turns
    # and the chat model's messages are "user" turns.
    flipped_history = []
    for msg in conversation_history:
        flipped_role = "assistant" if msg["role"] == "user" else "user"
        flipped_history.append({"role": flipped_role, "content": msg["content"]})

    messages = [{"role": "system", "content": SYNTHETIC_USER_SYSTEM_PROMPT}] + flipped_history

    response = client.chat.completions.create(
        model=SYNTHETIC_USER_MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()


def get_chat_model_response(conversation_history: list[dict]) -> str:
    """
    Ask the chat model for the next response given the conversation so far.

    Args:
        conversation_history: List of {"role": ..., "content": ...} dicts
                              where role is "user" (synthetic user) or "assistant" (chat model).

    Returns:
        The chat model's response as a plain string.
    """
    messages = [{"role": "system", "content": CHAT_MODEL_SYSTEM_PROMPT}] + conversation_history

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Main conversation loop
# ---------------------------------------------------------------------------

def run_conversation(num_rounds: int = 25, verbose: bool = True) -> dict:
    """
    Run a full conversation between the synthetic user and the chat model.

    The synthetic user always goes first. Each round consists of:
      1. Synthetic user sends a message
      2. Chat model responds

    Args:
        num_rounds: Number of back-and-forth rounds to generate.
        verbose:    If True, print each turn to the console.

    Returns:
        A dict with:
          - "config": metadata about the run
          - "conversation": list of turn dicts, each with {round, speaker, content}
    """
    # OpenAI-format history shared across both models
    openai_history: list[dict] = []
    turns: list[dict] = []

    for round_num in range(1, num_rounds + 1):
        if verbose:
            print(f"\n[Round {round_num}]")

        # --- Synthetic user turn ---
        user_message = get_synthetic_user_message(openai_history)
        openai_history.append({"role": "user", "content": user_message})
        turns.append({"round": round_num, "speaker": "synthetic_user", "content": user_message})

        if verbose:
            print(f"  Synthetic user: {user_message}")

        # --- Chat model turn ---
        model_response = get_chat_model_response(openai_history)
        openai_history.append({"role": "assistant", "content": model_response})
        turns.append({"round": round_num, "speaker": "chat_model", "content": model_response})

        if verbose:
            print(f"  Chat model:     {model_response}")

    return {
        "config": {
            "synthetic_user_model": SYNTHETIC_USER_MODEL,
            "chat_model": CHAT_MODEL,
            "num_rounds": num_rounds,
            "temperature": TEMPERATURE,
        },
        "conversation": turns,
    }
