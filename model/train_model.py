import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Load dataset
df = pd.read_csv("../data/processed_tweets.csv")

# Prepare data for modeling
numeric_features = ['text_length', 'word_count', 'hashtag_count', 'user_followers', 'user_friends', 'user_statuses', 'hour_of_day']
categorical_features = ['is_verified', 'has_media', 'day_of_week']

y = df['is_viral']

# Define preprocessing steps
numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# Train-test split
X = df[numeric_features + categorical_features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model.fit(X_train, y_train)

# Save trained model
with open("../model/viral_predictor_model.pkl", "wb") as f:
    pickle.dump(model, f)