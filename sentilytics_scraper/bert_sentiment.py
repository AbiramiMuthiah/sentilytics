# bert_sentiment.py

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax

# Load pre-trained BERT model for sentiment analysis
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)
    confidence, predicted_class = torch.max(probs, dim=1)
    label = "positive" if predicted_class.item() == 1 else "negative"
    return label, round(confidence.item(), 4)

# Load tweets
df = pd.read_csv("tweets.csv")

# Run predictions
bert_labels = []
bert_confidences = []

for tweet in df["text"]:
    label, conf = predict_sentiment(tweet)
    bert_labels.append(label)
    bert_confidences.append(conf)

# Add to DataFrame
df["bert_sentiment"] = bert_labels
df["bert_confidence"] = bert_confidences

# Save to new CSV
df.to_csv("tweets_bert.csv", index=False)
print("BERT-based sentiment analysis complete. Results saved to tweets_bert.csv")
