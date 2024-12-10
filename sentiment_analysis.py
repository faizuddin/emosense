import instaloader
import os
import pytesseract 
import pandas as pd


USERNAME = "faizgram"
SESSION_FILE = "session-faizgram"

L = instaloader.Instaloader()

try:
    L.load_session_from_file(username=USERNAME, filename=SESSION_FILE)
except FileNotFoundError as e:
    print("Session file not found. Please log in manually using Instaloader CLI.")
    exit()
except instaloader.ConnectionException as e:
   print(f"Connection exception {e}")
   exit()

def by_hashtag(hashtag, limit, profile_name=None, location=None):
    post_count = 0
    hashtag_posts = pd.DataFrame(columns=["Thumb", "Caption", "Comment"])
    thumbs = []
    captions = []
    comments = []
    dates = []

    posts = L.get_hashtag_posts(hashtag)

    for post in posts:
        if post.caption:
            thumbs.append(post.url)
            captions.append(post.caption)
            comments.append(post.comments)
            dates.append(post.date)
            # print(f"Extracted caption: {post.caption}")
        
        post_count += 1
        if post_count >= limit:
            break

    hashtag_posts["Thumb"] = thumbs
    hashtag_posts["Caption"] = captions
    hashtag_posts["Date"] = dates
    hashtag_posts["Comment"] = comments

    return hashtag_posts






