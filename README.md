# 🛡️ Fake News & Review Detection: AI-Powered Analysis System

> **Ensuring Digital Integrity with State-of-the-Art Machine Learning Analysis.**

Fake News & Review Detection is a comprehensive, production-grade detection system designed to combat the spread of misinformation and deceptive marketing. By leveraging advanced Natural Language Processing (NLP) and robust Machine Learning algorithms, this system provides users with an intuitive platform to verify the authenticity of news articles and product reviews in real-time.

---

## 📝 Project Description

In an era of information overload, distinguishing between fact and fiction is increasingly difficult. Fake News & Review Detection solves this problem by providing a centralized hub for content verification.

- **The Problem**: Viral fake news and computer-generated product reviews mislead public opinion and skew consumer trust.
- **The Solution**: An automated analysis pipeline that classifies text based on linguistic patterns, sentiment, and structural markers found in millions of verified datasets.
- **Why this Project?**: Unlike simple keyword filters, this project uses contextual ML models that adapt to various writing styles, providing a confidence score for every prediction.

---

## ✨ Features

- **📰 Fake News Analyst**: Detects propaganda and fabricated news stories using high-speed Passive-Aggressive classification.
- **⭐ Review Integrity Engine**: Identifies computer-generated (CG) or manipulated reviews to ensure authentic consumer feedback.
- **📊 Real-time Dashboard**: A futuristic, responsive UI for seamless interaction across all devices.
- **📜 Detection History**: Automated persistence of results to a MySQL database for auditing and trend analysis.
- **🧠 Advanced NLP Pipeline**: Integrated NLTK-driven preprocessing including stop-word removal and lemmatization.
- **⚡ High Performance API**: RESTful endpoints for easy integration with third-party applications.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Glassmorphism), JavaScript (ES6+) |
| **Backend** | Python 3.x, Flask, Flask-CORS |
| **Database** | MySQL 8.0+ (PyMySQL) |
| **ML Libraries** | scikit-learn, joblib, pandas, numpy |
| **NLP** | NLTK (Natural Language Toolkit) |
| **Tools** | Git, pip, Virtualenv |

---

## 🏗️ System Architecture

The Fake News & Review Detection system follows a decoupled architecture ensuring scalability and reliability:

1.  **Presentation Layer (Frontend)**: User inputs text or news links via a modern web interface.
2.  **Logic Layer (API)**: Flask server receives POST requests and forwards text to the ML module.
3.  **Analysis Layer (ML)**: 
    - Text is cleaned and vectorized using **TF-IDF**.
    - **Passive-Aggressive Classifier** analyzes news.
    - **Logistic Regression** analyzes reviews.
4.  **Data Layer (Database)**: Results are timestamped and stored in the `detection_history` table in MySQL.

---

## 📂 Project Folder Structure

```text
truthguard/
├── app.py              # Main Flask server & Route management
├── config.py           # Database credentials & Static configs
├── setup_db.py         # One-time database & table initialization
├── requirements.txt    # Project dependencies
├── database/           
│   └── db_handler.py   # Database CRUD operations
├── ml/                 
│   ├── news_detector.py    # Prediction logic for news
│   ├── review_detector.py  # Prediction logic for reviews
│   └── preprocess.py       # Reusable text cleaning functions
├── models/             
│   ├── train_*.py          # Training scripts for ML models
│   └── *.pkl               # Serialized model and vectorizer files
├── static/             
│   ├── css/            # Futuristic UI stylesheets
│   └── js/             # Frontend logic & API calls
└── templates/          
    └── *.html          # Jinja2 based page templates
```

- `database/`: Handles all MySQL connections and queries.
- `ml/`: Contains the core "brain" of the application.
- `models/`: Stores the intelligence (weights) of the trained AI.
- `static/`: Visual and interactive assets for the user.

---

## ⚙️ Installation Guide

Follow these steps to set up the project on your local machine:

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/fake-news-detection.git
cd truthguard
```

**Step 2: Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Download NLP Data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**Step 5: Setup Database Configuration**
Open `config.py` and update your MySQL credentials:
```python
DB_USER = "your_username"
DB_PASSWORD = "your_password"
```

**Step 6: Initialize Database**
```bash
python setup_db.py
```

---

## 🚀 How to Run the Project

1.  **Ensure MySQL is running** in the background.
2.  **Train the Models** (Required if `.pkl` files are missing):
    ```bash
    python models/train_news_model.py
    python models/train_review_model.py
    ```
3.  **Start the Backend & Server**:
    ```bash
    python app.py
    ```
4.  **Access the Dashboard**:
    Open `http://localhost:5000` in your web browser.

---

## 📖 Usage Guide

1.  **Landing Page**: Navigate the futuristic dashboard to select "News Detection" or "Review Detection".
2.  **Input Content**: Paste the text of the article or product review into the analysis box.
3.  **Analyze**: Click the **"Analyze"** button. The system triggers the AI models.
4.  **Result View**: View the classification (REAL/FAKE) and the confidence score (%).
5.  **History**: Visit the **History** tab to see your past analysis reports.

---

## 🔗 API Documentation

### Detect Fake News
**Endpoint**: `POST /api/detect/news`  
**Description**: Analyzes a news article return a prediction.

**Request Example**:
```json
{
  "text": "The moon is made of green cheese according to a new NASA report..."
}
```

**Response Example**:
```json
{
  "result": "FAKE",
  "confidence": 98.4,
  "status": "success"
}
```

### Detect Fake Review
**Endpoint**: `POST /api/detect/review`  
**Request Example**: `{"text": "Best product ever! I love it so much!"}`

---

## 📸 Screenshots

| Landing Page | Detection Result |
| :---: | :---: |
| ![Landing Page Placeholder](https://via.placeholder.com/400x250?text=Landing+Page) | ![Result Placeholder](https://via.placeholder.com/400x250?text=Detection+Result) |

---

## 🚢 Deployment Guide

- **Frontend/Backend**: This is a monolithic Flask app. You can deploy it using **Render** or **Railway**.
- **Database**: Use **MySQL on Clever Cloud** or **PlanetScale** for a managed database.
- **Environment Variables**: Use a `.env` file for production `DB_PASSWORD` and `SECRET_KEY`.

---

## 🔧 Troubleshooting

- **MySQL Connection Failed**: Ensure your `config.py` password matches your MySQL root password and the service is running.
- **Missing Models**: If you see a `file not found` error for `.pkl` files, ensure you have run the training scripts in the `models/` directory.
- **NLTK Error**: Run the NLTK download command provided in Step 4 of the installation guide.

---

## 🔮 Future Improvements

- [ ] Support for **URL Scraping**: Automatically fetch news text from a given link.
- [ ] **Image Deepfake Detection**: Identifying manipulated images in news articles.
- [ ] **Multi-language Support**: Expanding detection to Spanish, French, and Hindi.
- [ ] **Browser Extension**: Real-time checking while you surf the web.

---

## 👥 Contributors
- **BCA EXPERT** - Lead Developer & Documentation Creator

---

## 📄 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📧 Contact Information
For inquiries or support, please contact:
- **Email**: support@fakenewsdetection.ai
- **Website**: [fakenewsdetection.ai](http://localhost:5000)
- **LinkedIn**: [BCA EXPERT](https://linkedin.com/in/yourprofile)

---
*Built with ❤️ for a more truthful digital world.*
