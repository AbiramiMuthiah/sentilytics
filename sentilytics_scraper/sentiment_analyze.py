import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load comments from JSON
with open("youtube_comments.json", "r", encoding="utf-8") as f:
    comments = json.load(f)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Analyze sentiments
for comment in comments:
    score = analyzer.polarity_scores(comment["text"])
    comment["sentiment_score"] = score["compound"]
    comment["sentiment_label"] = (
        "Positive" if score["compound"] >= 0.05 else
        "Negative" if score["compound"] <= -0.05 else
        "Neutral"
    )

# Save results to CSV
df = pd.DataFrame(comments)
df.to_csv("youtube_comments_sentiment.csv", index=False)

print("✅ Sentiment analysis complete. Results saved to youtube_comments_sentiment.csv")
