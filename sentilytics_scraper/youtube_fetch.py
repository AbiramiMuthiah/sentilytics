import os
import json
import pandas as pd
from googleapiclient.discovery import build

# Set up your API key
API_KEY = 'AIzaSyAbrxk0_p1Aea0x_Qg0m_12r6TrYndYIt0'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# 🔍 Define the search topic and parameters
search_query = 'AI OR ChatGPT OR data science'
max_videos = 5  # Number of videos to fetch

print("🔍 Searching for videos...")

# Step 1: Search videos by keyword
search_response = youtube.search().list(
    q=search_query,
    part='id,snippet',
    maxResults=max_videos,
    type='video',
    order='relevance'
).execute()

video_ids = [item['id']['videoId'] for item in search_response['items']]

print(f"✅ Found {len(video_ids)} videos. Now fetching comments...")

# Step 2: Fetch comments for each video
all_comments = []

for video_id in video_ids:
    next_page_token = None
    while True:
        try:
            comment_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat='plainText'
            ).execute()

            for item in comment_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                all_comments.append({
                    'video_id': video_id,
                    'author': comment.get('authorDisplayName'),
                    'text': comment.get('textDisplay'),
                    'published_at': comment.get('publishedAt'),
                    'like_count': comment.get('likeCount')
                })

            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"⚠️ Error fetching comments for video {video_id}: {e}")
            break

print(f"💬 Total comments fetched: {len(all_comments)}")

# Step 3: Save to JSON
with open('youtube_comments.json', 'w', encoding='utf-8') as f:
    json.dump(all_comments, f, ensure_ascii=False, indent=4)

print("✅ Comments saved to youtube_comments.json")
