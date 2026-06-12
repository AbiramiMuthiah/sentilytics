import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from langdetect import detect, DetectorFactory
from urllib.parse import urlparse, parse_qs
import torch
import os
import plotly.express as px

# --- 💡 Load Custom CSS if available ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("custom.css")

# --- 🔐 OpenAI Setup ---
from openai import OpenAI
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_summary(comments):
    prompt = f"Summarize the tone and sentiment in the following YouTube comments:\n{comments}\n\nIn bullet points."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- 🌐 Page Setup ---
DetectorFactory.seed = 0
st.set_page_config(page_title="YouTube Sentiment AI", layout="wide")

# --- 📦 Load BERT Model ---
@st.cache_resource
def load_bert():
    try:
        tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
        model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading BERT model: {e}")
        return None, None

tokenizer, model = load_bert()

# --- 🧠 Sentiment Function ---
def get_sentiment(texts):
    sentiments, scores = [], []
    for i in range(0, len(texts), 16):
        batch = texts[i:i+16]
        enc = tokenizer(batch, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            output = model(**enc)
        probs = softmax(output.logits.numpy(), axis=1)
        for p in probs:
            score = p.argmax() + 1
            sentiments.append("Positive" if score > 3 else "Neutral" if score == 3 else "Negative")
            scores.append(float(p.max()))
    return sentiments, scores

# --- 🧠 OpenAI Summary ---
def generate_summary(comments):
    prompt = f"Summarize the tone and sentiment in the following YouTube comments:\n{comments}\n\nIn bullet points."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# --- 🔗 YouTube Comment Fetch ---
def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    elif "youtube.com" in parsed.hostname:
        return parse_qs(parsed.query).get("v", [None])[0]
    return None

def fetch_comments(video_id, api_key, max_results=100):
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "textFormat": "plainText",
        "key": api_key
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        items = res.json().get("items", [])
        return pd.DataFrame([{
            "author": c["snippet"]["topLevelComment"]["snippet"].get("authorDisplayName", ""),
            "text": c["snippet"]["topLevelComment"]["snippet"].get("textDisplay", ""),
            "published_at": c["snippet"]["topLevelComment"]["snippet"].get("publishedAt", "")
        } for c in items])
    else:
        st.error(f"Error fetching comments: {res.status_code}")
    return pd.DataFrame()

# --- 🖥️ Sidebar ---
st.sidebar.header("YouTube Sentiment Setup")
api_key = st.sidebar.text_input("🔑 Enter Your API Key", type="password")
video_url = st.sidebar.text_input("📺 Paste YouTube Video URL")
fetch_btn = st.sidebar.button("🔍 Fetch Comments")

# --- 🎯 Main Content ---
st.markdown("<h1 style='color:#E50914;'>YouTube Sentiment AI</h1>", unsafe_allow_html=True)

if fetch_btn and api_key and video_url:
    video_id = get_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL format.")
    else:
        with st.spinner("Fetching comments..."):
            df = fetch_comments(video_id, api_key)

        if df.empty:
            st.warning("No comments found or invalid video ID.")
        else:
            with st.spinner("Analyzing sentiments using BERT..."):
                df["sentiment"], df["score"] = get_sentiment(df["text"].astype(str).tolist())

            # --- 📌 Summary ---
            st.markdown("### Summary of Comments")
            summary_text = generate_summary("\n".join(df["text"].head(20)))
            st.info(summary_text)

            # --- 📊 Sentiment Charts ---
            st.markdown("### Sentiment Analysis")
            sentiment_counts = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"]).fillna(0)

            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots(figsize=(3.5, 2.5))
                ax.bar(sentiment_counts.index, sentiment_counts.values, color=["#32CD32", "#FFD700", "#FF0000"])
                ax.set_title("Sentiment Counts", color="white", fontsize=10)
                ax.set_facecolor("#0F0F0F")
                ax.tick_params(colors="white")
                st.pyplot(fig)

            with col2:
                fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
                ax2.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
                        colors=["#32CD32", "#FFD700", "#FF0000"],
                        textprops={'color': "white", 'fontsize': 9})
                ax2.set_facecolor("#0F0F0F")
                st.pyplot(fig2)

            # --- 📝 Data Table ---
            st.markdown("### Comments Table")
            st.dataframe(df[["author", "text", "sentiment", "score"]], use_container_width=True)

            # --- 🔍 Filter ---
            st.markdown("### Filter Comments by Sentiment")
            sentiment_filter = st.selectbox("Choose sentiment to filter:", ["All", "Positive", "Neutral", "Negative"])
            if sentiment_filter != "All":
                filtered_df = df[df["sentiment"] == sentiment_filter]
            else:
                filtered_df = df

            st.dataframe(filtered_df[["author", "text", "sentiment", "score"]], use_container_width=True)

            # --- 📥 Export ---
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Filtered CSV", csv, file_name="sentiment_results.csv", mime="text/csv")
