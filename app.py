# ═══════════════════════════════════════════════════════════
# Fake News and Review Detector — Flask Application
# ═══════════════════════════════════════════════════════════
#
# HOW TO RUN
# ──────────
# Step 1: pip install -r requirements.txt
# Step 2: python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
# Step 3: Set your MySQL password in config.py
# Step 4: python setup_db.py
# Step 5: Download datasets (see datasets/README.md)
# Step 6: python models/train_news_model.py
# Step 7: python models/train_review_model.py
# Step 8: python app.py
# Step 9: Open http://localhost:5000
#

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename


from ml.news_detector import predict_news
from ml.review_detector import predict_review
from database.db_handler import save_result, get_history

# ── App factory ─────────────────────────────────────────────
app = Flask(__name__)
CORS(app)



# ═════════════════════════════════════════════════════════════
#  PAGE ROUTES — render HTML templates
# ═════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/news")
def news_page():
    return render_template("news.html")


@app.route("/reviews")
def reviews_page():
    return render_template("reviews.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


# ═════════════════════════════════════════════════════════════
#  API ROUTES — return JSON
# ═════════════════════════════════════════════════════════════

@app.route("/api/detect/news", methods=["POST"])
def api_detect_news():
    """Analyse a news article and return REAL/FAKE prediction."""
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Text is required."}), 400

        result = predict_news(text)

        # Persist to database
        save_result(
            detection_type="news",
            input_text=text[:500],          # truncate for storage
            result=result["result"],
            confidence=result["confidence"],
        )
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500


@app.route("/api/detect/review", methods=["POST"])
def api_detect_review():
    """Analyse a product review and return REAL/FAKE prediction."""
    try:
        data = request.get_json(force=True)
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "Text is required."}), 400

        result = predict_review(text)

        save_result(
            detection_type="review",
            input_text=text[:500],
            result=result["result"],
            confidence=result["confidence"],
        )
        return jsonify(result), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """Return the most recent detection history records."""
    try:
        rows = get_history(limit=50)
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500


# ═════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
