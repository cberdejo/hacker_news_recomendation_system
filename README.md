# 📰 Hacker News Recommender System
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)


[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

This project implements a **news recommendation system** using **natural language processing (NLP)** techniques and **vector storage** with **Qdrant**. It uses **web scraping** to extract news from [Hacker News (Algolia)](https://hn.algolia.com) and recommends articles to users based on a simulated reading history.

## 🚀 Technologies and Models Used

- **Web scraping**: Selenium for extracting news from the web.
- **NLP**: spaCy for keyword extraction (relevant nouns).
- **Embeddings**: `average_word_embeddings_komninos` model from `sentence-transformers`.
- **Vector database**: Qdrant (local disk storage).
- **Language**: Python 3.11+

## 🧠 How the System Works

1. **Scraping Titles**: Automatically crawls Hacker News and extracts news titles.
2. **Text Processing**:
   - Uses embeddings via `SentenceTransformer`.
   - Extracts 2–4 *keywords* per article using spaCy.
3. **Vectorization and Storage**: Titles and keywords are stored as vectors in Qdrant.
4. **User Simulation**:
   - Generates keywords and an average embedding based on a fictional user reading history.
5. **Recommendation**:
   - Queries the closest vectors in Qdrant, filtering by the user’s predominant *keywords*.

## 📦 Installation

If `uv` is not installed, follow these steps:

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/Scripts/activate
```

2. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

3. Make sure Chrome and its [compatible driver](https://chromedriver.chromium.org/downloads) are installed.

## ⚙️ Running the Project

If using `uv`:
```bash
uv run src/main.py
```

Otherwise:
```bash
python src/main.py
```

This script:
- Scrapes news if the Qdrant collection is empty.
- Processes titles and extracts embeddings and keywords.
- Simulates a user history.
- Generates personalized recommendations based on semantic similarity and keywords.

## 📁 Module Separation

This project can be split into three parts:
- **scraper.py**: Contains all the scraping and processing logic.
- **recommender.py**: Contains the logic for Qdrant interactions, preprocessing, recommendation algorithm, etc.
- **main.py**: Example program that uses functions from scraper.py and recommender.py

## 📌 Notes

- The embeddings model (`komninos`) has a size of 300 and is optimized for efficiency.
- Filtering by *keywords* allows recommendations to be more relevant and thematically focused.
- Storage in Qdrant is persistent (folder `./data`).

