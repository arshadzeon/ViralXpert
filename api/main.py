import os
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Build the path dynamically
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/viral_predictor_model.pkl")

with open("model/viral_predictor_model.pkl", "rb") as f:
    model = pickle.load(f)
    
# Define input schema
class TweetData(BaseModel):
    text: str
    hashtags: list
    hour_of_day: int

# Preprocess text
def preprocess_text(text):
    return text.lower()

# Feature extraction
def extract_features(data: TweetData):
    processed_text = preprocess_text(data.text)
    text_length = len(processed_text)
    word_count = len(processed_text.split())
    hashtag_count = len(data.hashtags)
    
    return [[text_length, word_count, hashtag_count, data.hour_of_day]]

# API to predict tweet virality
@app.post("/predict/")
def predict_viral_tweet(tweet: TweetData):
    features = extract_features(tweet)
    prediction = model.predict(features)[0]  # 1 = Viral, 0 = Not Viral
    return {"is_viral": bool(prediction)}

# API to provide optimization insights
@app.post("/optimize/")
def optimize_tweet(tweet: TweetData):
    insights = {
        "Optimal Tweet Length": 120,
        "Ideal Hashtag Count": 2,
        "Best Posting Hour": 15,
        "Most Common Words in Viral Tweets": ["growth", "AI", "startup"]
    }
    return insights