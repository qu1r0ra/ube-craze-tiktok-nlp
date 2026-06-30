"""Sentiment Analysis module using CardiffNLP XLM-RoBERTa model locally."""

from typing import Any

import torch
from transformers import pipeline

# Constants
MODEL_NAME = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

# Mapping CardiffNLP output labels to human-readable sentiments
LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive",
}


class SentimentAnalyzer:
    def __init__(self, model_name: str = MODEL_NAME, batch_size: int = 16):
        self.model_name = model_name
        self.batch_size = batch_size
        self.device = 0 if torch.cuda.is_available() else -1
        self._pipeline = None

    @property
    def pipeline(self):
        """Lazy-loaded transformers sentiment pipeline."""
        if self._pipeline is None:
            print(f"Loading sentiment model: {self.model_name} on device: {self.device}...")
            # Disable pipeline warning messages
            self._pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=self.device,
            )
        return self._pipeline

    def predict(self, text: str) -> dict[str, Any]:
        """Predict sentiment of a single text string."""
        if not text.strip():
            return {"label": "neutral", "score": 0.0}

        try:
            # The pipeline returns a list containing a dict,
            # e.g., [{'label': 'LABEL_1', 'score': 0.85}]
            res = self.pipeline(text)[0]
            mapped_label = LABEL_MAP.get(res["label"], "neutral")
            return {"label": mapped_label, "score": float(res["score"])}
        except Exception as e:
            print(f"Error predicting sentiment: {e}")
            return {"label": "neutral", "score": 0.0}

    def predict_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """Predict sentiment of a batch of text strings efficiently."""
        if not texts:
            return []

        # Replace empty strings with a space to avoid pipeline crashes
        sanitized_texts = [t if t.strip() else " " for t in texts]

        results = []
        try:
            # Run batch inference
            pipe_results = self.pipeline(
                sanitized_texts,
                batch_size=self.batch_size,
                truncation=True,
                max_length=512,
            )
            for res in pipe_results:
                mapped_label = LABEL_MAP.get(res["label"], "neutral")
                results.append({"label": mapped_label, "score": float(res["score"])})
        except Exception as e:
            print(f"Error during batch sentiment prediction: {e}")
            # Fallback to single predictions
            results = [self.predict(t) for t in texts]

        return results


# Global analyzer singleton instance
_analyzer = None


def get_analyzer(batch_size: int = 16) -> SentimentAnalyzer:
    """Helper to get or initialize the global SentimentAnalyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentAnalyzer(batch_size=batch_size)
    return _analyzer


def analyze_sentiment(text: str) -> dict[str, Any]:
    """Helper to analyze a single text string."""
    return get_analyzer().predict(text)


def analyze_sentiment_batch(texts: list[str]) -> list[dict[str, Any]]:
    """Helper to analyze a list of text strings."""
    return get_analyzer().predict_batch(texts)
