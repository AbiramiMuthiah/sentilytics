import streamlit as st
import pandas as pd
import requests
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# --- Function to extract YouTube video ID from URL ---
def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

# --- Function to fetch comments using YouTube Data API v3 ---
def fetch_youtube_comments(video_id, api_key, max_results=100):
    comments = []
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "key": api_key,
        "maxResults": 100,
        "textFormat": "plainText"
    }
    while url and len(comments) < max_results:
        response = requests.get(url, params=params).json()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment.get("authorDisplayName"),
                "text": comment.get("textDisplay"),
                "published_at": comment.get("publishedAt")
            })
        # Next page
        next_page = response.get("nextPageToken")
        if next_page:
            params["pageToken"] = next_page
        else:
            break
    return comments

# --- Function to analyze sentiment ---
def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

# --- Live YouTube Analysis UI ---
st.subheader("🔴 Live YouTube Video Analysis")

video_url = st.text_input("Paste YouTube Video URL", placeholder="https://www.youtube.com/watch?v=abc123XYZ")
analyze_button = st.button("Fetch & Analyze Comments")

if analyze_button and video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ Invalid YouTube URL.")
    else:
        st.info("Fetching comments... Please wait.")
        api_key = st.secrets["YOUTUBE_API_KEY"]
        raw_comments = fetch_youtube_comments(video_id, api_key)

        if not raw_comments:
            st.warning("No comments found or video is private.")
        else:
            df_live = pd.DataFrame(raw_comments)
            df_live["sentiment"], df_live["compound"] = zip(*df_live["text"].apply(analyze_sentiment))
            df_live["published_at"] = pd.to_datetime(df_live["published_at"])

            st.success(f"Fetched {len(df_live)} comments!")

            # Show in table
            st.dataframe(df_live[["author", "text", "sentiment", "compound"]])

            # Download
            st.download_button(
                label="Download as Excel",
                data=df_live.to_csv(index=False).encode("utf-8"),
                file_name="live_youtube_comments.csv",
                mime="text/csv"
            )
