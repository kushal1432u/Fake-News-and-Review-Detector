# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Text Preprocessing Module
# ═══════════════════════════════════════════════════════════
# Cleans raw text for NLP model input: lowercasing, stripping
# non-alpha characters, tokenising, and removing stopwords.

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data (safe to call multiple times)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

# Cache the stopword set once at module level
_STOP_WORDS = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """
    Pre-process a raw string for TF-IDF vectorisation.

    Steps:
        1. Lowercase the text
        2. Remove all non-alphabetic characters
        3. Tokenise with NLTK word_tokenize
        4. Remove English stopwords
        5. Return the cleaned, space-joined string
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()                             # 1. lowercase
    text = re.sub(r"[^a-z\s]", "", text)            # 2. keep only letters + spaces
    tokens = word_tokenize(text)                    # 3. tokenise
    tokens = [t for t in tokens if t not in _STOP_WORDS]  # 4. drop stopwords
    return " ".join(tokens)                         # 5. rejoin
