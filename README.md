<div align="center">

# Sentilytics

### Multilingual YouTube Comment Sentiment Analysis Platform

<p align="center">
  A real-time sentiment analysis dashboard that extracts YouTube comments and classifies them using <strong>BERT</strong> and <strong>VADER</strong> — with AI-generated audience summaries and interactive analytics.
</p>

<br/>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/BERT-blueviolet?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Transformers-FFB000?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas"/>

![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)
![Language](https://img.shields.io/badge/Python-97%25-blue?style=flat-square)

</div>

---

## Overview

Sentilytics is a sentiment analysis platform that analyzes YouTube comments in real time. It fetches comments from any YouTube video, runs them through a BERT and VADER NLP pipeline, and visualizes audience sentiment through an interactive Streamlit dashboard.

The platform supports multilingual comments and generates AI-powered summaries of overall audience reaction, making it useful for content creators, marketers, and researchers.

---

## Key Features

### Sentiment Analysis Engine

- BERT-based sentiment classification (Positive / Neutral / Negative)
- VADER scoring for fast lexical sentiment estimation
- Multilingual comment support
- Confidence scores per classification

### YouTube Comment Scraper

- YouTube Data API integration
- Bulk comment extraction from any public video
- Automated text preprocessing pipeline
- Language detection support

### Interactive Dashboard

- Real-time sentiment breakdown charts (pie + bar)
- Searchable and filterable comment table
- Sentiment distribution by comment volume
- CSV export for further analysis
- Dark-themed modern UI built with Streamlit

### AI Summary

- OpenAI-generated audience reaction summary
- Overall tone interpretation
- Key sentiment drivers highlighted

---

## Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

### Login

![Login](assets/login.png)

## System Architecture

```
YouTube Video URL
        |
YouTube Data API
        |
Comment Extraction (sentilytics_scraper)
        |
+----------------------------------+
|  Text Preprocessing              |
|  BERT Sentiment Classification   |
|  VADER Sentiment Scoring         |
|  OpenAI Summary Generation       |
+----------------------------------+
        |
Streamlit Analytics Dashboard
        |
CSV Export
```

---

## Tech Stack

| Category        | Technologies              |
| --------------- | ------------------------- |
| AI / NLP        | BERT, Transformers, VADER |
| AI Summary      | OpenAI API                |
| Dashboard       | Streamlit                 |
| Data Processing | Pandas, NumPy             |
| Visualization   | Plotly, Matplotlib        |
| APIs            | YouTube Data API v3       |
| Language        | Python                    |
| Tools           | GitHub, VS Code           |

---

## Getting Started

### Prerequisites

- Python 3.9+
- YouTube Data API key (free at [console.cloud.google.com](https://console.cloud.google.com))
- OpenAI API key (optional — for AI summary feature)

### 1. Clone the Repository

```bash
git clone https://github.com/AbiramiMuthiah/sentilytics.git
cd sentilytics
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
# Windows
set YOUTUBE_API_KEY=your_youtube_api_key
set OPENAI_API_KEY=your_openai_api_key

# Mac/Linux
export YOUTUBE_API_KEY=your_youtube_api_key
export OPENAI_API_KEY=your_openai_api_key
```

### 4. Run the Dashboard

```bash
streamlit run sentilytics/app.py
# Opens at http://localhost:8501
```

---

## Project Structure

```
sentilytics/
├── sentilytics/
│   └── sentilytics_scraper/   # YouTube comment extraction
│       ├── scraper.py         # YouTube Data API integration
│       ├── preprocessor.py    # Text cleaning pipeline
│       └── sentiment.py       # BERT + VADER classification
├── requirements.txt
└── README.md
```

---

## Future Improvements

- Multi-platform support (Twitter/X, Reddit, Instagram)
- Real-time live stream comment analysis
- Emotion detection (beyond positive/negative/neutral)
- Fine-tuned multilingual BERT model
- User authentication and saved analysis history
- Cloud deployment on Streamlit Cloud or AWS

---

## Author

**Abirami Muthiah**  
Applied AI Engineer | NLP | Data Science

[![Portfolio](https://img.shields.io/badge/Portfolio-abiramimuthiah--portfolio.vercel.app-blue?style=flat-square)](https://abiramimuthiah-portfolio.vercel.app)
[![GitHub](https://img.shields.io/badge/GitHub-AbiramiMuthiah-181717?style=flat-square&logo=github)](https://github.com/AbiramiMuthiah)

---

## License

Licensed under the [MIT License](LICENSE).
