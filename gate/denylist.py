import re

from rapidfuzz import fuzz

DENYLIST_TERMS = ["examplecorp"]


def normalize_text(text: str) -> str:
    """Normalize case and punctuation for denylist matching."""
    return re.sub(r"[^\w\s]", "", text.casefold())


def contains_denylisted_term(text: str) -> bool:
    """Detect denylisted words and phrases, including close matches."""
    normalized_text = normalize_text(text)
    words = normalized_text.split()

    for term in DENYLIST_TERMS:
        normalized_term = normalize_text(term)
        term_words = normalized_term.split()

        if not term_words:
            continue

        window_size = len(term_words)

        for start in range(len(words) - window_size + 1):
            candidate = " ".join(words[start : start + window_size])

            if candidate == normalized_term:
                return True

            if (
                len(normalized_term) >= 5
                and fuzz.ratio(candidate, normalized_term) >= 90
            ):
                return True

    return False
