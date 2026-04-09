"""
logger.py — Save and load conversation data as JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path

from src.config import DATA_DIR


def save_conversation(conversation_data: dict, run_id: str) -> str:
    """
    Save a conversation dict to a timestamped JSON file.

    Args:
        conversation_data: Output from run_conversation().
        run_id:            Unique label for this run (used in the filename).

    Returns:
        The filepath where the file was saved.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{run_id}_{timestamp}.json"
    filepath = os.path.join(DATA_DIR, filename)

    # Annotate the data before saving
    output = {
        "run_id": run_id,
        "timestamp": timestamp,
        **conversation_data,
    }

    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Conversation saved to: {filepath}")
    return filepath


def load_conversation(filepath: str) -> dict:
    """
    Load a conversation from a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        The conversation data as a dict.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def list_conversations(data_dir: str = DATA_DIR) -> list[str]:
    """
    List all saved conversation JSON files, sorted by modification time (newest first).

    Args:
        data_dir: Directory to scan.

    Returns:
        List of filepaths.
    """
    directory = Path(data_dir)
    if not directory.exists():
        return []

    files = sorted(directory.glob("*.json"), key=os.path.getmtime, reverse=True)
    return [str(f) for f in files]
