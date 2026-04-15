"""
evaluation.py — Compute basic metrics for each generated response.

No external dependencies or extra API calls. Add new metric functions here;
conversation_generator.py only calls evaluate_response().
"""

from datetime import datetime, timezone
import re

# ---------------------------------------------------------------------------
# Sentiment word lists
# ---------------------------------------------------------------------------

_POSITIVE_WORDS = {
    "great", "amazing", "excellent", "wonderful", "fantastic", "awesome",
    "love", "happy", "good", "nice", "beautiful", "best", "brilliant",
    "glad", "enjoy", "enjoyed", "exciting", "excited", "perfect", "superb",
    "delightful", "pleased", "positive", "thankful", "grateful", "fun",
}

_NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "difficult", "hard", "worst",
    "hate", "sad", "unfortunate", "disappoint", "disappointed", "disappointing",
    "frustrating", "frustrated", "frustration", "annoying", "annoyed",
    "negative", "problem", "problems", "fail", "failed", "failure",
    "boring", "bored", "worried", "worry", "concern", "concerned",
}


# ---------------------------------------------------------------------------
# Metric functions
# ---------------------------------------------------------------------------

def compute_response_length(text: str) -> dict:
    """Return token_count (whitespace-split), word_count (alpha tokens), char_count."""
    tokens = text.split()
    words = [t for t in tokens if re.search(r"[a-zA-Z]", t)]
    return {
        "token_count": len(tokens),
        "word_count": len(words),
        "char_count": len(text),
    }


def compute_lexical_diversity(text: str) -> float:
    """Return unique_words / total_words (0–1). Returns 0.0 for empty text."""
    words = [w.lower() for w in re.findall(r"[a-zA-Z]+", text)]
    if not words:
        return 0.0
    return round(len(set(words)) / len(words), 4)


def compute_sentiment(text: str) -> str:
    """
    Simple keyword heuristic.
    Returns 'positive', 'negative', or 'neutral'.
    """
    words = {w.lower() for w in re.findall(r"[a-zA-Z]+", text)}
    pos_hits = len(words & _POSITIVE_WORDS)
    neg_hits = len(words & _NEGATIVE_WORDS)
    if pos_hits > neg_hits:
        return "positive"
    if neg_hits > pos_hits:
        return "negative"
    return "neutral"


# ---------------------------------------------------------------------------
# Master evaluation function
# ---------------------------------------------------------------------------

def evaluate_response(text: str, speaker: str) -> dict:
    """
    Run all metrics on a single response.

    Args:
        text:    The response content.
        speaker: Who produced the response (for context; not used in computation).

    Returns:
        {
            length:    { token_count, word_count, char_count },
            diversity: float,
            sentiment: "positive" | "neutral" | "negative",
            timestamp: ISO-8601 UTC string,
        }
    """
    return {
        "length": compute_response_length(text),
        "diversity": compute_lexical_diversity(text),
        "sentiment": compute_sentiment(text),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
