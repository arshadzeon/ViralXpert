import pandas as pd
import re

# Text preprocessing
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)  # Remove mentions
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.lower()

# Feature Engineering
def engineer_features(df):
    df_features = df.copy()
    
    df_features['processed_text'] = df_features['text'].apply(preprocess_text)
    df_features['text_length'] = df_features['processed_text'].apply(len)
    df_features['word_count'] = df_features['processed_text'].apply(lambda x: len(x.split()))
    df_features['hashtag_count'] = df_features['hashtags'].apply(len)
    
    df_features['engagement_rate'] = (df_features['retweet_count'] + df_features['favorite_count']) / (df_features['user_followers'] + 1)
    
    df_features['hour_of_day'] = df_features['created_at'].dt.hour
    df_features['day_of_week'] = df_features['created_at'].dt.dayofweek
    
    engagement_threshold = df_features['engagement_rate'].quantile(0.75)
    df_features['is_viral'] = df_features['engagement_rate'] > engagement_threshold
    
    return df_features

