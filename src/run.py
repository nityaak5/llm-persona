"""
run.py — CLI entry point for the conversation generation pipeline.

Usage examples:
  python src/run.py --rounds 25 --run_id test_001
  python src/run.py --rounds 50 --run_id experiment_01
  python src/run.py --list
  python src/run.py --rounds 10 --run_id quick_test --quiet
"""

import argparse
import sys

import os
import sys

# Allow running as: python src/run.py from the repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import DEFAULT_NUM_ROUNDS, DATA_DIR
from src.conversation_generator import run_conversation
from src.logger import save_conversation, list_conversations


def main():
    parser = argparse.ArgumentParser(
        description="Generate conversations between a synthetic user and a chat model."
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=DEFAULT_NUM_ROUNDS,
        help=f"Number of conversation rounds (default: {DEFAULT_NUM_ROUNDS})",
    )
    parser.add_argument(
        "--run_id",
        type=str,
        default="test_run",
        help="Unique identifier for this run (used in the saved filename)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-turn console output",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all saved conversations and exit",
    )
    args = parser.parse_args()

    # --list: show saved conversations and exit
    if args.list:
        files = list_conversations(DATA_DIR)
        if not files:
            print("No saved conversations found.")
        else:
            print(f"Saved conversations ({len(files)} total):")
            for f in files:
                print(f"  {f}")
        sys.exit(0)

    # Run conversation
    print(f"Starting conversation: run_id={args.run_id}, rounds={args.rounds}")
    conversation_data = run_conversation(num_rounds=args.rounds, verbose=not args.quiet)

    # Save to disk
    filepath = save_conversation(conversation_data, run_id=args.run_id)

    # Summary
    total_turns = len(conversation_data["conversation"])
    print(f"\nDone. {args.rounds} rounds ({total_turns} turns) saved to: {filepath}")


if __name__ == "__main__":
    main()
