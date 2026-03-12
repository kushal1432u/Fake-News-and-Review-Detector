# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Fake-News Model Training Script
# ═══════════════════════════════════════════════════════════
# Usage:  python models/train_news_model.py
#
# Expects two CSVs in datasets/:
#   fake_news.csv  (columns: title, text)  → labelled FAKE
#   true_news.csv  (columns: title, text)  → labelled REAL
#
# Outputs:
#   models/news_model.pkl   — trained PassiveAggressiveClassifier
#   models/tfidf_news.pkl   — fitted TfidfVectorizer

import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
import joblib

# Allow imports from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ml.preprocess import clean_text  # noqa: E402


def train():
    """Train a Passive-Aggressive classifier on fake / real news data."""

    # ── 1. Load datasets ────────────────────────────────────
    fake_path = os.path.join("datasets", "fake_news.csv")
    true_path = os.path.join("datasets", "true_news.csv")

    if not os.path.exists(fake_path) or not os.path.exists(true_path):
        print("ERROR: Place fake_news.csv and true_news.csv in the datasets/ folder.")
        print("       See datasets/README.md for download instructions.")
        sys.exit(1)

    df_fake = pd.read_csv(fake_path)
    df_true = pd.read_csv(true_path)

    # Add labels
    df_fake["label"] = "FAKE"
    df_true["label"] = "REAL"

    # ── 2. Merge & shuffle ──────────────────────────────────
    df = pd.concat([df_fake, df_true], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Use 'text' column; fall back to 'title' if 'text' is missing
    text_col = "text" if "text" in df.columns else "title"
    df["clean"] = df[text_col].astype(str).apply(clean_text)

    # ── 3. Train / test split ───────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2, random_state=42
    )

    # ── 4. TF-IDF vectorisation ─────────────────────────────
    tfidf = TfidfVectorizer(max_features=5000)
    X_train_tfidf = tfidf.fit_transform(X_train)
    X_test_tfidf = tfidf.transform(X_test)

    # ── 5. Train classifier ─────────────────────────────────
    model = PassiveAggressiveClassifier(max_iter=50)
    model.fit(X_train_tfidf, y_train)

    # ── 6. Evaluate ─────────────────────────────────────────
    preds = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, preds)
    print(f"News model accuracy: {acc * 100:.2f}%")

    # ── 7. Save artefacts ───────────────────────────────────
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, os.path.join("models", "news_model.pkl"))
    joblib.dump(tfidf, os.path.join("models", "tfidf_news.pkl"))
    print("Saved  →  models/news_model.pkl")
    print("Saved  →  models/tfidf_news.pkl")


if __name__ == "__main__":
    train()
