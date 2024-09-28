import requests
import os
import time
import tweepy
import anthropic
from urllib.parse import urlparse

# Twitter Authentication
def authenticate_twitter(consumer_key, consumer_secret, access_token, access_token_secret):
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    return client

# Rephrase Tweet using Claude (Anthropic API)
def rephrase_text_with_claude(api_key, text):
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": "Rephrase this text in only 1 way, and write it directly: " + text
            }
        ]
    )

    rephrased_text = message.content[0].text
    return rephrased_text

# Download media file from URL
def download_media(media_url):
    parsed_url = urlparse(media_url)
    file_name = os.path.basename(parsed_url.path)
    file_path = f"./media/{file_name}"

    if not os.path.exists('./media'):
        os.makedirs('./media')

    response = requests.get(media_url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return file_path

# Post Tweet with optional media
def post_rephrased_content(client, text, media_files=None):
    if len(text) > 280:
        text = text[:277] + "..."
    
    media_ids = []
    
    # Upload media files to Twitter
    if media_files:
        for file_path in media_files:
            media_response = client.media_upload(file_path)
            media_ids.append(media_response.media_id)
    
    # Post the tweet with media
    response = client.create_tweet(text=text, media_ids=media_ids)
    print(f"Tweet posted successfully: {response.data}")

# Post all rephrased tweets with media
def post_scraped_tweets(client, claude_api_key, tweets_data):
    for tweet in tweets_data:
        tweet_text = tweet['text']
        print(f"Original Tweet: {tweet_text}")
        
        # Rephrase tweet using Claude
        rephrased_text = rephrase_text_with_claude(claude_api_key, tweet_text)
        print(f"Rephrased Text: {rephrased_text}")

        # Download media files from tweet (if present)
        media_files = []
        for media_url in tweet.get('media_urls', []):
            media_files.append(download_media(media_url))
        
        # Post rephrased tweet with media
        post_rephrased_content(client, rephrased_text, media_files)

        # Remove downloaded media files after posting
        for file_path in media_files:
            os.remove(file_path)

        # Sleep to avoid rate limits
        time.sleep(60)
