# YouTube Sentiment Analysis - Quick Start Guide

## Prerequisites
- Python 3.12+
- Chrome/Chromium browser
- YouTube Data API v3 key
- Both repositories cloned

## Project Structure
```
/Users/lokimandloi/Desktop/Youtube/
├── yt-sentiment-analysis/          # Flask backend
│   ├── flask_app/
│   │   └── app_simple.py           # Main Flask server
│   └── venv/                        # Python virtual environment
└── yt-chrome-plugin-frontend/      # Chrome extension
    ├── manifest.json
    ├── popup.html
    ├── popup.js
    └── background.js
```

## Step 1: Start Flask Backend

### Terminal 1: Start the Flask Server
```bash
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app
/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/venv/bin/python app_simple.py
```

**Expected output:**
```
Loading vectorizer...
Vectorizer not found at ./tfidf_vectorizer.pkl
Warning: Vectorizer not loaded. Using rule-based sentiment analysis.

============================================================
YouTube Sentiment Analysis API - Simplified Version
============================================================
Starting Flask app on http://0.0.0.0:5005
============================================================

 * Serving Flask app 'app_simple'
 * Debug mode: on
 * Running on http://0.0.0.0:5005
```

### Verify Backend is Running
```bash
curl http://localhost:5005/health
```

**Expected response:**
```json
{
  "model_loaded": true,
  "status": "healthy",
  "vectorizer_loaded": false
}
```

## Step 2: Load Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Navigate to: `/Users/lokimandloi/Desktop/Youtube/yt-chrome-plugin-frontend`
5. Click "Select" to load the extension

## Step 3: Use the Extension

1. Go to any YouTube video with comments
2. Click the **YouTube Comment Analyzer** extension icon in Chrome toolbar
3. The popup will:
   - Fetch all comments from the video
   - Send them to Flask backend for sentiment analysis
   - Display results with:
     - Sentiment distribution (pie chart)
     - Word cloud
     - Sentiment trend over time
     - Metrics (positive/negative/neutral counts)

## Available API Endpoints

All endpoints run on `http://localhost:5005`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check server status |
| `/predict` | POST | Analyze sentiment of comments |
| `/predict_with_timestamps` | POST | Analyze sentiment with timestamps |
| `/generate_chart` | GET | Generate sentiment pie chart |
| `/generate_wordcloud` | GET | Generate word cloud |
| `/generate_trend_graph` | GET | Generate sentiment trend graph |

## Test Sentiment Analysis

```bash
curl -X POST http://localhost:5005/predict \
  -H "Content-Type: application/json" \
  -d '{
    "comments": [
      "this is amazing!",
      "this is terrible",
      "ok neutral"
    ]
  }'
```

**Expected response:**
```json
[
  {"comment": "this is amazing!", "sentiment": "1"},
  {"comment": "this is terrible", "sentiment": "-1"},
  {"comment": "ok neutral", "sentiment": "0"}
]
```

## Sentiment Values
- `1` = Positive 😊
- `-1` = Negative ☹️
- `0` = Neutral 😐

## Configuration

### Flask Backend Port
Edit `app_simple.py` to change port if needed (currently: 5005)

### Extension UI Width
Edit `popup.html` to change popup width (currently: 700px)

```html
<style>
  body {
    width: 700px;  /* Change this value */
  }
</style>
```

### YouTube API Key
The extension uses the YouTube Data API v3. Ensure your API key is properly configured in `popup.js`:
```javascript
const YOUTUBE_API_KEY = 'YOUR_API_KEY_HERE';
```

## Troubleshooting

### Flask not responding
```bash
# Kill all Python processes
killall -9 python

# Wait 2 seconds
sleep 2

# Restart Flask
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app
/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/venv/bin/python app_simple.py
```

### Port 5005 already in use
```bash
# Find and kill process using port 5005
lsof -i :5005 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Extension not loading
1. Go to `chrome://extensions/`
2. Find the extension and click reload
3. Clear Chrome cache (Ctrl+Shift+Delete)
4. Reload the YouTube page

### No comments fetched
- Ensure the YouTube video has comments enabled
- Check the browser console (F12) for API errors
- Verify YouTube Data API quota hasn't been exceeded

## Next Steps

After confirming everything works:
1. Test on multiple YouTube videos
2. Verify sentiment analysis accuracy
3. Check visualizations quality
4. Ready for RoBERTa model integration when needed
