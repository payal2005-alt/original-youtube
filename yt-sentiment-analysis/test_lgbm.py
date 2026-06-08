#!/usr/bin/env python
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the LightGBM model
model_path = "/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/mlruns/966942924428166701/bd036fefc0f14357b78a244de908eb24/artifacts/lgbm_model/model.pkl"
vectorizer_path = "/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/mlruns/966942924428166701/bd036fefc0f14357b78a244de908eb24/artifacts/vectorizer/tfidf_vectorizer.pkl"

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print(f"✅ Model loaded from: {model_path}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

try:
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    print(f"✅ Vectorizer loaded")
except Exception as e:
    print(f"❌ Error loading vectorizer: {e}")
    exit(1)

# Test comments
test_comments = [
    "This video is amazing! Love it!",  # Should be positive
    "This is absolute garbage",  # Should be negative
    "Not very good content",  # Should be negative
    "Average video, could be better",  # Should be neutral
    "Subscribe now!",  # Should be positive
]

print("\nTesting LightGBM model predictions:")
print("-" * 60)

try:
    input_data = vectorizer.transform(test_comments)
    predictions = model.predict(input_data)
    
    sentiment_map = {
        -1: 'NEGATIVE',
        0: 'NEUTRAL',
        1: 'POSITIVE',
        2: 'REALLY_NEGATIVE'  # Some models use different encoding
    }
    
    print(f"{'Comment':<40} {'Prediction':<15}")
    print("-" * 60)
    
    for comment, pred in zip(test_comments, predictions):
        pred_int = int(pred)
        sentiment_label = sentiment_map.get(pred_int, f'UNKNOWN ({pred_int})')
        
        comment_short = comment[:35] + "..." if len(comment) > 35 else comment
        print(f"{comment_short:<40} {sentiment_label:<15}")
    
    print("\n" + "-" * 60)
    print(f"Unique predictions: {set(predictions)}")
    print(f"Classes found: {sorted(set(predictions))}")
    
except Exception as e:
    print(f"❌ Error during prediction: {e}")
    import traceback
    traceback.print_exc()
