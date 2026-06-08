import sys
import os
import traceback

sys.path.append(r'c:\Users\payal\Downloads\Youtube\yt-sentiment-analysis\flask_app')

try:
    import app
    print("SUCCESS")
    print("Model:", type(app.model))
    print("Vectorizer:", type(app.vectorizer))
except Exception as e:
    print("ERROR LOADING APP:")
    traceback.print_exc()
