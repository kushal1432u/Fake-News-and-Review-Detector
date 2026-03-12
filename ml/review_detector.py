# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Review Detector (inference)
# ═══════════════════════════════════════════════════════════
# Loads the pre-trained LogisticRegression and TF-IDF
# vectoriser, then exposes predict_review(text).

import os
import joblib
from ml.preprocess import clean_text

# ── Load model & vectoriser at module level ─────────────────
_MODEL_PATH = os.path.join("models", "review_model.pkl")
_TFIDF_PATH = os.path.join("models", "tfidf_reviews.pkl")

_model = None
_tfidf = None

if os.path.exists(_MODEL_PATH) and os.path.exists(_TFIDF_PATH):
    _model = joblib.load(_MODEL_PATH)
    _tfidf = joblib.load(_TFIDF_PATH)


def predict_review(text: str) -> dict:
    """
    Predict whether a product review is REAL or FAKE.

    Returns:
        dict with keys 'result' ("REAL" / "FAKE") and 'confidence' (float %).
    """
    if _model is None or _tfidf is None:
        raise RuntimeError(
            "Review model not found. Run  python models/train_review_model.py  first."
        )

    cleaned = clean_text(text)
    vec = _tfidf.transform([cleaned])

    prediction = _model.predict(vec)[0]                         # "REAL" or "FAKE"
    proba = _model.predict_proba(vec)[0]                        # array of class probs
    confidence = round(float(max(proba)) * 100, 2)              # best probability

    return {"result": prediction, "confidence": confidence}
