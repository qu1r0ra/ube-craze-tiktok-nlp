# Project Overview & Architecture

Explores **digital gastronationalism** on TikTok regarding the global **Ube** trend via comment scraper and multilingual sentiment NLP (English, Tagalog, Taglish).

## Domain Guidelines

- **Scraper**: Playwright network interception targeting `/api/comment/list/` (`src/ube_craze_nlp/scraper/engine.py`).
- **NLP & Sentiment**: Lingua (EN/TL identification), `stopwordsiso` + `nltk` (stopwords), and local `cardiffnlp/twitter-xlm-roberta-base-sentiment`.
- **Notebook Pipeline**: Sequential notebooks `01_scraping.ipynb` through `04_visualization.ipynb`.
