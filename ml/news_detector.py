# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — News Detector (inference)
# ═══════════════════════════════════════════════════════════
# Loads the pre-trained PassiveAggressiveClassifier and
# TF-IDF vectoriser, then exposes predict_news(text).

import os
import math
import joblib
from ml.preprocess import clean_text

# ── Load model & vectoriser at module level ─────────────────
_MODEL_PATH = os.path.join("models", "news_model.pkl")
_TFIDF_PATH = os.path.join("models", "tfidf_news.pkl")

_model = None
_tfidf = None

if os.path.exists(_MODEL_PATH) and os.path.exists(_TFIDF_PATH):
    _model = joblib.load(_MODEL_PATH)
    _tfidf = joblib.load(_TFIDF_PATH)


def _sigmoid(x: float) -> float:
    """Map decision-function score to a 0-1 probability via sigmoid."""
    return 1.0 / (1.0 + math.exp(-x))


def predict_news(text: str) -> dict:
    """
    Predict whether a news article is REAL or FAKE.

    Returns:
        dict with keys 'result' ("REAL" / "FAKE") and 'confidence' (float %).
    """
    if _model is None or _tfidf is None:
        raise RuntimeError(
            "News model not found. Run  python models/train_news_model.py  first."
        )

    cleaned = clean_text(text)
    vec = _tfidf.transform([cleaned])

    prediction = _model.predict(vec)[0]                # "REAL" or "FAKE"
    score = _model.decision_function(vec)[0]           # raw score
    confidence = round(_sigmoid(abs(score)) * 100, 2)  # 50-100 %
    
    sources = []
    try:
        from ddgs import DDGS
        query_text = text.strip()[:150]
        results = DDGS().text(query_text, max_results=3)
        
        match_found = False
        query_words = set(query_text.lower().split())
        
        max_overlap = 0
        for r in results:
            href = r.get('href', '')
            if href and href not in sources:
                sources.append(href)
            
            title_words = set(r.get('title', '').lower().split())
            overlap = len(query_words.intersection(title_words))
            if overlap > max_overlap:
                max_overlap = overlap
            if overlap >= 3:
                match_found = True
                
        if prediction == "FAKE" and match_found:
            prediction = "REAL"
            confidence = min(99.9, 80.0 + (max_overlap * 2))

    except Exception as e:
        print("DDGS fetch error:", e)

    return {"result": str(prediction), "confidence": confidence, "sources": sources}
