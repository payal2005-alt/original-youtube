# YouTube Sentiment Analysis - Chrome Extension Integration Guide

## 🎯 Project Structure

```
/Users/payal/Downloads/Youtube/
├── yt-sentiment-analysis/          # ML Backend (Flask API)
│   ├── flask_app/
│   │   ├── app.py                  # Flask API Server (Port 5005)
│   │   └── requirements.txt
│   ├── models/                     # Trained ML models
│   ├── src/                        # Data processing & training scripts
│   ├── requirements.txt
│   └── venv/                       # Virtual environment
│
└── yt-chrome-plugin-frontend/      # Chrome Extension
    ├── manifest.json               # Extension configuration
    ├── popup.html                  # Extension UI
    ├── popup.js                    # Extension logic (connects to Flask API)
    └── images/                     # Extension assets
```

---

## 🔧 Integration Overview

The integration works as follows:

```
User opens YouTube video
    ↓
Clicks Chrome Extension
    ↓
Extension extracts Video ID
    ↓
Extension fetches comments using YouTube Data API
    ↓
Extension sends comments to Flask API (http://localhost:5005/predict_with_timestamps)
    ↓
Flask API performs sentiment analysis
    ↓
Extension displays results: sentiment distribution, metrics, visualizations
```

---

## 📋 Flask API Endpoints (Backend)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Welcome message & model status |
| `/health` | GET | Health check (model & vectorizer loaded) |
| `/predict` | POST | Predict sentiment for comments |
| `/predict_with_timestamps` | POST | Predict sentiment with timestamps |
| `/generate_chart` | POST | Generate sentiment distribution pie chart |
| `/generate_wordcloud` | POST | Generate word cloud from comments |
| `/generate_trend_graph` | POST | Generate sentiment trend over time |

---

## ✅ Prerequisites Setup

### 1. Backend (Already Done)
- ✅ Repository cloned to `/Users/payal/Download/Youtube/yt-sentiment-analysis`
- ✅ Virtual environment created (`venv/`)
- ✅ Dependencies installed
- ✅ Flask API ready on port 5005

### 2. Chrome Extension
- ✅ Repository cloned to `/Users/payal/Download/Youtube/yt-chrome-plugin-frontend`
- ⚠️ Needs YouTube Data API key (for fetching comments)
- ⚠️ Needs to be loaded into Chrome

### 3. YouTube Data API Key
You need a Google API key to fetch YouTube comments:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy the API key

---

## 🚀 Step-by-Step Integration

### Step 1: Ensure Flask API is Running

The Flask API should be running on port 5005:

```bash
cd /Users/payal/Downloads/Youtube/yt-sentiment-analysis/flask_app
source ../venv/bin/activate
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5005
```

### Step 2: Update Chrome Extension with YouTube API Key

Edit the file: `/Users/payal/Downloads/Youtube/yt-chrome-plugin-frontend/popup.js`

Find this line (around line 5):
```javascript
const API_KEY = 'your_api_key';  // Replace with your actual YouTube Data API key
```

Replace `'your_api_key'` with your actual YouTube Data API key:
```javascript
const API_KEY = 'AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
```

### Step 3: Load Chrome Extension

1. **Open Chrome Extensions Page**
   - Go to: `chrome://extensions/`
   - OR: Menu → More Tools → Extensions

2. **Enable Developer Mode**
   - Toggle the "Developer mode" switch in the top-right corner

3. **Load Unpacked Extension**
   - Click "Load unpacked"
   - Navigate to: `/Users/payal/Downloads/Youtube/yt-chrome-plugin-frontend`
   - Select the folder and click "Open"

4. **Verify Extension Loaded**
   - You should see "YouTube Comment Analyzer" in your extensions list
   - Extension icon will appear in Chrome toolbar

### Step 4: Test the Integration

1. **Start Flask API** (if not already running):
   ```bash
   cd /Users/payal/Downloads/Youtube/yt-sentiment-analysis/flask_app
   source ../venv/bin/activate
   python app.py
   ```

2. **Visit a YouTube Video**
   - Go to any YouTube video page
   - Example: https://www.youtube.com/watch?v=dQw4w9WgXcQ

3. **Click Extension Icon**
   - Click the "YouTube Comment Analyzer" extension in your toolbar
   - A popup will appear

4. **Expected Results**
   - ✅ Video ID displayed
   - ✅ Comments fetched (if video has comments)
   - ✅ Sentiment analysis performed
   - ✅ Results displayed with:
     - Sentiment counts (Positive/Neutral/Negative)
     - Metrics (total comments, unique commenters, avg sentiment)
     - Visualizations

---

## 🔄 API Communication Flow

### Request Format (Extension → Flask)

**Endpoint:** `POST /predict_with_timestamps`

```json
{
  "comments": [
    {
      "text": "This tutorial is really helpful!",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "text": "This didn't work for me",
      "timestamp": "2024-01-15T10:31:00Z"
    }
  ]
}
```

### Response Format (Flask → Extension)

```json
[
  {
    "comment": "This tutorial is really helpful!",
    "sentiment": "1",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  {
    "comment": "This didn't work for me",
    "sentiment": "-1",
    "timestamp": "2024-01-15T10:31:00Z"
  }
]
```

**Sentiment Values:**
- `"1"` = Positive
- `"0"` = Neutral
- `"-1"` = Negative

---

## 🐛 Troubleshooting

### Issue: Extension shows "Cannot connect to Flask API"

**Solution:**
1. Check Flask API is running on port 5005:
   ```bash
   curl http://localhost:5005/health
   ```
2. Should return:
   ```json
   {
     "status": "healthy",
     "model_loaded": true,
     "vectorizer_loaded": true
   }
   ```
3. If connection fails, restart Flask API

### Issue: "Model or vectorizer not loaded"

**Solution:**
1. Ensure model files exist in `/models/` and `/flask_app/`
2. Check MLflow tracking URI is correctly set
3. Verify `tfidf_vectorizer.pkl` exists
4. Restart Flask API

### Issue: No comments found for video

**Solution:**
1. YouTube video's comments might be disabled
2. Try a different video with more comments
3. Check YouTube API quota hasn't been exceeded

### Issue: Extension blocked by CORS

**Solution:**
1. Flask API has CORS enabled (`flask_cors`)
2. If still blocked, check browser console for specific error
3. Ensure API_URL in popup.js is `http://localhost:5005`

---

## 📊 File Locations Summary

| Component | Location | Port |
|-----------|----------|------|
| Flask Backend | `/yt-sentiment-analysis/flask_app/app.py` | 5005 |
| Chrome Extension | `/yt-chrome-plugin-frontend/popup.js` | - |
| Models | `/yt-sentiment-analysis/models/` | - |
| Vectorizer | `/yt-sentiment-analysis/flask_app/tfidf_vectorizer.pkl` | - |

---

## 🔐 Security Notes

- API key should not be hardcoded in production
- Use environment variables for API keys
- Example `.env` file can be created for sensitive data
- Never commit API keys to version control

---

## 🎨 Customization Options

### Modify Extension UI
- Edit: `/yt-chrome-plugin-frontend/popup.html` (styles)
- Edit: `/yt-chrome-plugin-frontend/popup.js` (logic)

### Change Flask Port
- Edit: `/yt-sentiment-analysis/flask_app/app.py` (last line)
- Update: `/yt-chrome-plugin-frontend/popup.js` (API_URL)

### Add New API Endpoints
- Edit: `/yt-sentiment-analysis/flask_app/app.py`
- Add corresponding calls in popup.js

---

## ✨ Next Steps

1. ✅ Get YouTube Data API key
2. ✅ Update popup.js with API key
3. ✅ Load extension into Chrome
4. ✅ Test on a YouTube video
5. 🔄 Iterate and customize as needed

---

**Ready to analyze YouTube sentiment! 🚀**
