# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Fake-Review Model Training Script
# ═══════════════════════════════════════════════════════════
# Usage:  python models/train_review_model.py
#
# Expects: datasets/reviews.csv
#   columns: text, label   (label values: CG → FAKE, OR → REAL)
#
# Outputs:
#   models/review_model.pkl    — trained LogisticRegression
#   models/tfidf_reviews.pkl   — fitted TfidfVectorizer

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.preprocess import clean_text  # noqa: E402


def train():
    """Train a Logistic Regression classifier on fake / real reviews."""

    # ── 1. Load dataset ─────────────────────────────────────
    csv_path = os.path.join("datasets", "reviews.csv")

    if not os.path.exists(csv_path):
        print("ERROR: Place reviews.csv in the datasets/ folder.")
        print("       See datasets/README.md for download instructions.")
        sys.exit(1)

    df = pd.read_csv(csv_path)

    # Map labels: CG (computer-generated) → FAKE, OR (original) → REAL
    label_map = {"CG": "FAKE", "OR": "REAL"}
    if df["label"].isin(["CG", "OR"]).any():
        df["label"] = df["label"].map(label_map).fillna(df["label"])

    # ── 2. Clean text ───────────────────────────────────────
    df["clean"] = df["text_"].astype(str).apply(clean_text)

    # ── 3. Train / test split ───────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2, random_state=42
    )

    # ── 4. TF-IDF vectorisation ─────────────────────────────
    tfidf = TfidfVectorizer(max_features=3000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # ── 5. Train classifier ─────────────────────────────────
    model = LogisticRegression(max_iter=200)
    model.fit(X_train_tfidf, y_train)

    # ── 6. Evaluate ─────────────────────────────────────────
    preds = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, preds)
    print(f"Review model accuracy: {acc * 100:.2f}%")

    # ── 7. Save artefacts ───────────────────────────────────
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, os.path.join("models", "review_model.pkl"))
    joblib.dump(tfidf, os.path.join("models", "tfidf_reviews.pkl"))
    print("Saved  →  models/review_model.pkl")
    print("Saved  →  models/tfidf_reviews.pkl")


if __name__ == "__main__":
    train()
