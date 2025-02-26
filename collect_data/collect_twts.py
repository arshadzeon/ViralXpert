import tweepy
import pandas as pd
import time

# API Authentication (Replace with actual keys)
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to collect tweets
def collect_tweets(keywords, count=100):
    all_tweets = []
    
    for keyword in keywords:
        tweets = api.search_tweets(q=keyword, count=count, tweet_mode='extended')
        
        for tweet in tweets:
            tweet_data = {
                'id': tweet.id,
                'text': tweet.full_text,
                'created_at': tweet.created_at,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count,
                'user_followers': tweet.user.followers_count,
                'user_friends': tweet.user.friends_count,
                'user_statuses': tweet.user.statuses_count,
                'hashtags': [hashtag['text'] for hashtag in tweet.entities['hashtags']],
                'has_media': 'media' in tweet.entities if hasattr(tweet, 'entities') else False,
                'is_verified': tweet.user.verified
            }
            all_tweets.append(tweet_data)

        time.sleep(2)  # Avoid rate limits
    
    return pd.DataFrame(all_tweets)

