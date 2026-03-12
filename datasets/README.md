# Fake News and Review Detector — Dataset Download Instructions

## 1. Fake News Dataset

**Source:** [Kaggle — Fake and Real News Dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

### Steps
1. Visit the link above and click **Download** (you need a free Kaggle account).
2. Extract the ZIP. You will get two files:
   - `Fake.csv` → **rename to** `fake_news.csv`
   - `True.csv` → **rename to** `true_news.csv`
3. Place both CSV files in this `datasets/` folder.

### Required Columns
| Column | Description |
|--------|-------------|
| `title` | Headline of the article |
| `text`  | Full article body |

> The training script (`models/train_news_model.py`) automatically adds a `label` column (`FAKE` / `REAL`).

---

## 2. Fake Reviews Dataset

**Source:** [Kaggle — Fake Reviews Dataset](https://www.kaggle.com/datasets/mexwell/fake-reviews-dataset)

### Steps
1. Visit the link above and click **Download**.
2. Extract the ZIP. You will get `reviews.csv`.
3. Place `reviews.csv` in this `datasets/` folder.

### Required Columns
| Column  | Description |
|---------|-------------|
| `text`  | Review body |
| `label` | `CG` = computer-generated (fake), `OR` = original (real) |

> The training script (`models/train_review_model.py`) remaps `CG → FAKE` and `OR → REAL`.

---

## Final Folder Contents

After downloading, your `datasets/` folder should look like:

```
datasets/
├── README.md          ← this file
├── fake_news.csv
├── true_news.csv
└── reviews.csv
```

Then run the training scripts from the project root:

```bash
python models/train_news_model.py
python models/train_review_model.py
```
