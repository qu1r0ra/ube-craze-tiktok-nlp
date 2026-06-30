"""Language filtering, text normalization, and stopword removal module."""

import re

import nltk
from lingua import Language, LanguageDetectorBuilder
from stopwordsiso import stopwords

# Ensure NLTK tokenizers are available
for resource in ["tokenizers/punkt", "tokenizers/punkt_tab"]:
    try:
        nltk.data.find(resource)
    except LookupError:
        name = resource.split("/")[-1]
        nltk.download(name, quiet=True)

# Build a language detector for English, Tagalog, and neighboring/foreign languages
# This helps distinguish and filter out non-target languages while keeping Taglish
# (which gets classified as EN or TL)
TARGET_LANGS = [Language.ENGLISH, Language.TAGALOG]
FILTERED_LANGS = [
    Language.INDONESIAN,
    Language.MALAY,
    Language.SPANISH,
    Language.VIETNAMESE,
    Language.JAPANESE,
    Language.CHINESE,
    Language.KOREAN,
    Language.THAI,
    Language.PORTUGUESE,
]

# Create global detector instance
detector = LanguageDetectorBuilder.from_languages(*(TARGET_LANGS + FILTERED_LANGS)).build()

# Load stopword lists
ENGLISH_STOPWORDS = set(stopwords("en"))
TAGALOG_STOPWORDS = set(stopwords("tl"))
ALL_STOPWORDS = ENGLISH_STOPWORDS.union(TAGALOG_STOPWORDS)


def detect_language(text: str) -> str | None:
    """Detect the language of the text. Returns 'en', 'tl', or 'other' (or None)."""
    if not text.strip():
        return None

    # Pre-clean text slightly for language detector (remove URLs/usernames)
    temp_text = re.sub(r"http\S+|www\S+", "", text)
    temp_text = re.sub(r"@\w+", "", temp_text).strip()

    if not temp_text:
        return None

    try:
        detected = detector.detect_language_of(temp_text)
        if detected == Language.ENGLISH:
            return "en"
        elif detected == Language.TAGALOG:
            return "tl"
        elif detected is not None:
            return "other"
    except Exception as e:
        print(f"Error detecting language: {e}")
    return None


def is_target_language(text: str) -> bool:
    """Check if the text is in one of the target languages (English or Tagalog/Taglish)."""
    lang = detect_language(text)
    # If language detection is uncertain (None), we default to keeping it
    return lang in ("en", "tl", None)


def normalize_text(text: str, remove_emojis: bool = False) -> str:
    """Normalize text by removing URLs, usernames, extra whitespace, and optionally emojis."""
    if not text:
        return ""

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove TikTok usernames (@username)
    text = re.sub(r"@\w+", "", text)

    if remove_emojis:
        # Strip out non-ascii characters (coarse emoji removal)
        text = text.encode("ascii", "ignore").decode("ascii")

    # Remove duplicate spaces and strip
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_text(text: str) -> list[str]:
    """Tokenize text into lowercase words."""
    cleaned = normalize_text(text, remove_emojis=True)
    # Remove punctuation
    cleaned = re.sub(r"[^\w\s]", "", cleaned)
    tokens = nltk.word_tokenize(cleaned.lower())
    return tokens


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove English and Tagalog stopwords from a list of tokens."""
    return [token for token in tokens if token not in ALL_STOPWORDS and len(token) > 1]
