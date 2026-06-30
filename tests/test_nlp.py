"""Unit tests for the NLP cleaning and language detection modules."""

from unittest.mock import MagicMock, patch

from ube_craze_nlp.nlp.clean import (
    detect_language,
    is_target_language,
    normalize_text,
    remove_stopwords,
    tokenize_text,
)
from ube_craze_nlp.nlp.sentiment import SentimentAnalyzer


def test_normalize_text():
    """Test text normalization rules."""
    # Test URL removal
    assert (
        normalize_text("Check this out: https://example.com/ube and comment!")
        == "Check this out: and comment!"
    )
    # Test username removal
    assert normalize_text("Thanks for sharing @filipinofoodie! #ube") == "Thanks for sharing ! #ube"
    # Test whitespace compaction
    assert normalize_text("  This    has   too  many   spaces.  ") == "This has too many spaces."


def test_tokenize_text():
    """Test tokenization and cleaning."""
    text = "Ube Halaya is delicious! Yum yum."
    tokens = tokenize_text(text)
    assert tokens == ["ube", "halaya", "is", "delicious", "yum", "yum"]


def test_remove_stopwords():
    """Test stopword removal for Tagalog and English."""
    tokens = ["the", "ube", "craze", "is", "masarap", "mga", "sa", "ice", "cream"]
    cleaned = remove_stopwords(tokens)

    # English: 'the', 'is' are stopwords and should be removed
    # Tagalog: 'mga', 'sa' are stopwords and should be removed
    assert "the" not in cleaned
    assert "is" not in cleaned
    assert "mga" not in cleaned
    assert "sa" not in cleaned

    # Non-stopwords should be retained
    assert "ube" in cleaned
    assert "craze" in cleaned
    assert "masarap" in cleaned
    assert "ice" in cleaned
    assert "cream" in cleaned


def test_detect_language():
    """Test language detection on English, Tagalog, and foreign texts."""
    # English
    assert detect_language("This is a beautiful purple potato dessert.") == "en"
    # Tagalog
    assert detect_language("Masarap talaga kumain ng ube halaya tuwing Pasko.") == "tl"
    # Spanish (should be classified as 'other')
    assert detect_language("Este postre filipino es delicioso y de color morado.") == "other"


def test_is_target_language():
    """Test target language checker."""
    # English is a target
    assert is_target_language("I love purple yam ice cream.")
    # Tagalog is a target
    assert is_target_language("Gusto ko ng ube kakanin.")
    # Vietnamese is not a target
    assert not is_target_language("Món tráng miệng này rất ngon.")


@patch("ube_craze_nlp.nlp.sentiment.pipeline")
def test_sentiment_analyzer_mocked(mock_pipeline):
    """Test SentimentAnalyzer using a mocked pipeline to avoid model downloads."""
    # Configure mock pipeline response
    mock_pipe_instance = MagicMock()
    mock_pipe_instance.return_value = [{"label": "LABEL_2", "score": 0.98}]
    mock_pipeline.return_value = mock_pipe_instance

    analyzer = SentimentAnalyzer()
    res = analyzer.predict("This ube ice cream is amazing!")

    # Verify model loading parameters
    mock_pipeline.assert_called_with(
        "sentiment-analysis",
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        tokenizer="cardiffnlp/twitter-xlm-roberta-base-sentiment",
        device=analyzer.device,
    )

    # Verify predicted mapped label and score
    assert res["label"] == "positive"
    assert res["score"] == 0.98
