#!/usr/bin/env python
import sys
sys.path.insert(0, '/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis')

import mlflow
import mlflow.pyfunc
from mlflow.tracking import MlflowClient
import pandas as pd
import pickle
import os
import numpy as np

# Test comments with known sentiments
test_comments = [
    "This video is amazing! Love it!",  # Should be positive
    "This is absolute garbage", # Should be negative
    "Not very good content", # Should be negative
    "Average video, could be better", # Should be neutral
    "Subscribe now!", # Should be positive
]

# Load model and vectorizer
MODEL_NAME = "yt_chrome_plugin_model"
MODEL_STAGE = "staging"
VECTORIZER_PATH = "/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app/tfidf_vectorizer.pkl"

try:
    client = MlflowClient()
    model_uri = f"models:/{MODEL_NAME}@{MODEL_STAGE}"
    model = mlflow.pyfunc.load_model(model_uri)
    print(f"✅ Model loaded: {model_uri}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

try:
    with open(VECTORIZER_PATH, 'rb') as file:
        vectorizer = pickle.load(file)
    print(f"✅ Vectorizer loaded")
except Exception as e:
    print(f"❌ Error loading vectorizer: {e}")
    sys.exit(1)

# Transform and predict
print("\nTesting predictions:")
print("-" * 60)

try:
    input_data = vectorizer.transform(test_comments)
    input_df = pd.DataFrame(input_data.toarray(), columns=vectorizer.get_feature_names_out())
    predictions = model.predict(input_df)
    
    print(f"{'Comment':<40} {'Prediction':<15}")
    print("-" * 60)
    
    for comment, pred in zip(test_comments, predictions):
        sentiment_map = {-1: 'NEGATIVE', 0: 'NEUTRAL', 1: 'POSITIVE'}
        pred_int = int(pred)
        sentiment_label = sentiment_map.get(pred_int, f'UNKNOWN ({pred_int})')
        
        comment_short = comment[:35] + "..." if len(comment) > 35 else comment
        print(f"{comment_short:<40} {sentiment_label:<15}")
    
    print("\n" + "-" * 60)
    print(f"Unique predictions: {set(predictions)}")
    print(f"Prediction types: {[type(p) for p in predictions]}")
    
except Exception as e:
    print(f"❌ Error during prediction: {e}")
    import traceback
    traceback.print_exc()
