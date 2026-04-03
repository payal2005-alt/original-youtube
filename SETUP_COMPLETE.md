# ✅ YouTube Sentiment Analysis - COMPLETED SETUP

## 🎉 What Has Been Done

### 1. ✅ Backend Repository Cloned
- **Location:** `/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/`
- **Status:** Ready
- **Contains:** ML models, Flask API, DVC pipeline

### 2. ✅ Chrome Extension Repository Cloned  
- **Location:** `/Users/lokimandloi/Desktop/Youtube/yt-chrome-plugin-frontend/`
- **Status:** Ready
- **Contains:** Chrome extension UI and logic

### 3. ✅ Python Virtual Environment Created
- **Location:** `/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/venv/`
- **Status:** Active and configured

### 4. ✅ All Dependencies Installed
- Flask, NLTK, scikit-learn, pandas, matplotlib, wordcloud, and more
- Ready for API operations

---

## 🚀 Quick Start - Complete Integration in 3 Simple Steps

### **Step 1: Get YouTube Data API Key (5 minutes)**

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use existing)
3. Search for and enable "YouTube Data API v3"
4. Create API Credentials → API Key
5. Copy your API key (looks like: `AIzaSyD...xxxxx`)

### **Step 2: Update Chrome Extension**

Edit: `/Users/lokimandloi/Desktop/Youtube/yt-chrome-plugin-frontend/popup.js`

**Find this line (around line 5):**
```javascript
const API_KEY = 'your_api_key';
```

**Replace with your actual key:**
```javascript
const API_KEY = 'AIzaSyD...xxxxx';
```

Also check the API_URL (should be):
```javascript
const API_URL = 'http://localhost:5005';
```

### **Step 3: Load Extension into Chrome**

1. Open Chrome and go to: `chrome://extensions/`
2. **Enable Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select: `/Users/lokimandloi/Desktop/Youtube/yt-chrome-plugin-frontend/`
5. Click **Open** - Extension loaded! ✅

---

## 🔧 Starting the Flask Backend

### Option A: Start Flask from Terminal (Recommended for Development)

```bash
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app
source ../venv/bin/activate
python app_simple.py
```

**Expected Output:**
```
============================================================
YouTube Sentiment Analysis API - Simplified Version
============================================================
Starting Flask app on http://0.0.0.0:5005
============================================================

 * Serving Flask app 'app_simple'
 * Debug mode: on
 * Running on http://127.0.0.1:5005
 * Press CTRL+C to quit
```

### Option B: Use Run Task in VS Code

A VS Code task has been configured in your workspace

---

## 📋 Project Structure

```
/Users/lokimandloi/Desktop/Youtube/
│
├── yt-sentiment-analysis/              # Backend ML + API
│   ├── flask_app/
│   │   ├── app.py                     # Original (has MLflow complexity)
│   │   ├── app_simple.py              # Simplified version (USE THIS)
│   │   ├── app_test.py                # Minimal test app
│   │   └── tfidf_vectorizer.pkl       # ML model vectorizer (if exists)
│   ├── models/                        # Trained ML models
│   ├── src/                           # Training scripts
│   ├── venv/                          # Python virtual environment
│   └── README.md                      # Original documentation
│
├── yt-chrome-plugin-frontend/          # Browser Extension
│   ├── manifest.json                  # Extension config
│   ├── popup.html                     # UI markup
│   ├── popup.js                       # Chrome extension logic
│   └── images/                        # Icons & assets
│
├── INTEGRATION_GUIDE.md                # Detailed integration docs
└── SETUP_COMPLETE.md                  # This file
```

---

## 🧪 Testing the Integration

### 1. Start Flask API
```bash
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app
source ../venv/bin/activate
python app_simple.py
```

### 2. Test Health Check
```bash
curl http://localhost:5005/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "vectorizer_loaded": true/false
}
```

### 3. Open Chrome and Test Extension
1. Go to any YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
2. Click the "YouTube Comment Analyzer" extension icon
3. Extension will:
   - Extract video ID
   - Fetch comments using YouTube API
   - Send to Flask backend for analysis
   - Display sentiment results

---

## 📊 API Endpoints Available

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Welcome & status |
| `/health` | GET | Health check |
| `/predict` | POST | Sentiment prediction |
| `/predict_with_timestamps` | POST | Sentiment + timestamps |
| `/generate_chart` | POST | Sentiment pie chart |
| `/generate_wordcloud` | POST | Word cloud visualization |

---

## 🔐 Environment Variables (Optional)

For production, create `.env` file in flask_app/:

```bash
FLASK_ENV=production
FLASK_PORT=5005
YOUTUBE_API_KEY=your_key_here
```

---

## ⚠️ Troubleshooting

### Extension says "Cannot connect to Flask API"
```bash
# Check if Flask is running
curl http://localhost:5005/health

# If not running, start it:
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app
source ../venv/bin/activate
python app_simple.py
```

### No comments found on YouTube video
- Video might have comments disabled
- Try a different video with more comments
- Check YouTube API quota limits

### Port 5005 already in use
```bash
# Kill process using port 5005
lsof -i :5005
kill -9 <PID>
```

### Python module errors
```bash
# Reinstall dependencies
cd /Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

---

## 📚 Additional Resources

- **Main README**: `/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/README.md`
- **Integration Guide**: `/Users/lokimandloi/Desktop/Youtube/INTEGRATION_GUIDE.md`
- **Flask App**: `/Users/lokimandloi/Desktop/Youtube/yt-sentiment-analysis/flask_app/`
- **Extension Code**: `/Users/lokimandloi/Desktop/Youtube/yt-chrome-plugin-frontend/popup.js`

---

## ✨ What You Can Do Now

✅ Analyze YouTube video comments for sentiment  
✅ See sentiment distribution (positive/neutral/negative)  
✅ View comment metrics and statistics  
✅ Generate visualizations (pie charts, word clouds)  
✅ Use rule-based sentiment analysis (fallback)  
✅ Process comments with ML model (if vectorizer is loaded)  

---

## 🎯 Next Steps

1. **Get YouTube API key** (if you haven't)
2. **Update `popup.js`** with your API key
3. **Load extension** in Chrome
4. **Start Flask app**: `python app_simple.py`
5. **Visit a YouTube video** and click the extension
6. **Analyze comments!** 🎉

---

## 💡 Pro Tips

- Use `app_simple.py` instead of `app.py` to avoid environment issues
- Keep Flask terminal window open while using the extension
- The extension sends comments to Flask on port 5005 for analysis
- Rule-based sentiment works even without the ML model loaded
- Clear Chrome cache if extension doesn't update after changes

---

**Everything is configured and ready to go! Just need YouTube API key and you're all set! 🚀**
