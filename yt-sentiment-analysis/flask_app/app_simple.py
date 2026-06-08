# app_simple.py - Simplified Flask app without MLflow for Chrome Extension

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend before importing pyplot

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import joblib
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.dates as mdates
import os
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the preprocessing function
def preprocess_comment(comment):
    """Apply preprocessing transformations to a comment."""
    try:
        # Convert to lowercase
        comment = comment.lower()

        # Remove trailing and leading whitespaces
        comment = comment.strip()

        # Remove newline characters
        comment = re.sub(r'\n', ' ', comment)

        # Remove non-alphanumeric characters, except punctuation
        comment = re.sub(r'[^A-Za-z0-9\s!?.,]', '', comment)

        # Remove stopwords but retain important ones for sentiment analysis
        stop_words = set(stopwords.words('english')) - {'not', 'but', 'however', 'no', 'yet'}
        comment = ' '.join([word for word in comment.split() if word not in stop_words])

        # Lemmatize the words
        lemmatizer = WordNetLemmatizer()
        comment = ' '.join([lemmatizer.lemmatize(word) for word in comment.split()])

        return comment
    except Exception as e:
        print(f"Error in preprocessing comment: {e}")
        return comment

# Load the model and vectorizer
def load_model_and_vectorizer(vectorizer_path):
    """
    Load model and vectorizer from local path
    """
    try:
        # Try to load vectorizer from local path
        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            print(f"Successfully loaded vectorizer from {vectorizer_path}")
            return True, vectorizer
        else:
            print(f"Vectorizer not found at {vectorizer_path}")
            return False, None
        
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return False, None

# Initialize the model and vectorizer
try:
    VECTORIZER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tfidf_vectorizer.pkl")
    
    print("Loading vectorizer...")
    vectorizer_loaded, vectorizer = load_model_and_vectorizer(VECTORIZER_PATH)
    
    if vectorizer_loaded:
        print("Vectorizer loaded successfully!")
    else:
        print("Warning: Vectorizer not loaded. Using rule-based sentiment analysis.")
        vectorizer = None
    
except Exception as e:
    print(f"Failed to load vectorizer: {e}")
    vectorizer = None

def rule_based_sentiment(comment):
    """Improved rule-based sentiment analysis with better detection"""
    comment_lower = comment.lower()
    
    # Remove punctuation for better matching
    import re
    comment_clean = re.sub(r'[^\w\s]', ' ', comment_lower)
    
    # Positive and negative word lists
    positive_words = {
        'good', 'great', 'excellent', 'awesome', 'amazing', 'love', 'best', 'perfect', 'wonderful', 
        'fantastic', 'helpful', 'clear', 'easy', 'simple', 'works', 'thanks', 'thank', 'brilliant'
    }
    
    negative_words = {
        'bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'useless', 'broken', 'error', 
        'fail', 'failed', 'problem', 'issue', 'confusing', 'complicated', 'difficult'
    }
    
    # Count sentiment indicators
    pos_count = 0
    neg_count = 0
    
    # Check for positive words
    for pos_word in positive_words:
        if pos_word in comment_clean or pos_word in comment_lower:
            pos_count += 1
    
    # Check for negative words
    for neg_word in negative_words:
        if neg_word in comment_clean or neg_word in comment_lower:
            neg_count += 1
    
    # Check for common negations that flip sentiment
    negation_words = {'not', 'no', 'never', 'couldn\'t', 'can\'t', 'didn\'t', 'doesn\'t', 'won\'t', 'shouldn\'t'}
    has_negation = any(neg in comment_clean for neg in negation_words)
    
    # If negation found with positive words, reduce positive count
    if has_negation and pos_count > 0:
        pos_count = max(0, pos_count - 1)
    
    # Weighted sentiment calculation
    if pos_count > neg_count and pos_count > 0:
        return '1'  # Positive
    elif neg_count > pos_count and neg_count > 0:
        return '-1'  # Negative
    else:
        # Default to slight positive if any positive words, slight negative if any negative words
        if pos_count > 0:
            return '1'
        elif neg_count > 0:
            return '-1'
        else:
            return '0'  # Neutral

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to YouTube Sentiment Analysis API",
        "version": "1.0 (Simplified)",
        "vectorizer_loaded": vectorizer is not None
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "vectorizer_loaded": vectorizer is not None
    })

@app.route('/predict_with_timestamps', methods=['POST'])
def predict_with_timestamps():
    data = request.json
    comments_data = data.get('comments')
    
    if not comments_data:
        return jsonify({"error": "No comments provided"}), 400

    try:
        comments = [item['text'] for item in comments_data]
        timestamps = [item['timestamp'] for item in comments_data]

        # Preprocess and predict
        predictions = []
        for comment in comments:
            preprocessed = preprocess_comment(comment)
            if vectorizer:
                # Use vectorizer if available
                transformed = vectorizer.transform([preprocessed])
                # Simple heuristic: predict based on sum of features
                feature_sum = np.sum(transformed.toarray())
                if feature_sum > 0.5:
                    sentiment = '1'
                elif feature_sum < -0.5:
                    sentiment = '-1'
                else:
                    sentiment = '0'
            else:
                # Use rule-based sentiment
                sentiment = rule_based_sentiment(comment)
            
            predictions.append(sentiment)
        
        print(f"Processed {len(comments)} comments successfully")
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Return the response with original comments, predicted sentiments, and timestamps
    response = [
        {
            "comment": comment, 
            "sentiment": sentiment, 
            "timestamp": timestamp
        } 
        for comment, sentiment, timestamp in zip(comments, predictions, timestamps)
    ]
    return jsonify(response)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    comments = data.get('comments')
    
    if not comments:
        return jsonify({"error": "No comments provided"}), 400

    try:
        # Preprocess and predict
        predictions = []
        for comment in comments:
            preprocessed = preprocess_comment(comment)
            if vectorizer:
                # Use vectorizer if available
                transformed = vectorizer.transform([preprocessed])
                feature_sum = np.sum(transformed.toarray())
                if feature_sum > 0.5:
                    sentiment = '1'
                elif feature_sum < -0.5:
                    sentiment = '-1'
                else:
                    sentiment = '0'
            else:
                # Use rule-based sentiment
                sentiment = rule_based_sentiment(comment)
            
            predictions.append(sentiment)
        
        print(f"Processed {len(comments)} comments successfully")
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    
    # Return the response with original comments and predicted sentiments
    response = [
        {
            "comment": comment, 
            "sentiment": sentiment
        } 
        for comment, sentiment in zip(comments, predictions)
    ]
    return jsonify(response)

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        data = request.get_json()
        sentiment_counts = data.get('sentiment_counts')
        
        if not sentiment_counts:
            return jsonify({"error": "No sentiment counts provided"}), 400

        # Prepare data for the pie chart
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [
            int(sentiment_counts.get('1', 0)),
            int(sentiment_counts.get('0', 0)),
            int(sentiment_counts.get('-1', 0))
        ]
        
        if sum(sizes) == 0:
            raise ValueError("Sentiment counts sum to zero")
        
        colors = ['#36A2EB', '#C9CBCF', '#FF6384']  # Blue, Gray, Red

        # Generate the pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'color': 'white', 'fontsize': 10}
        )
        plt.title('Sentiment Distribution', color='white', fontsize=14)
        plt.axis('equal')
        
        # Set background color
        plt.gca().set_facecolor('#1e1e1e')
        plt.gcf().patch.set_facecolor('#1e1e1e')

        # Save the chart to a BytesIO object
        img_io = io.BytesIO()
        plt.savefig(img_io, format='PNG', facecolor='#1e1e1e', edgecolor='none', bbox_inches='tight')
        img_io.seek(0)
        plt.close()

        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"Error in /generate_chart: {e}")
        return jsonify({"error": f"Chart generation failed: {str(e)}"}), 500

@app.route('/generate_wordcloud', methods=['POST'])
def generate_wordcloud():
    try:
        data = request.get_json()
        comments = data.get('comments')

        if not comments:
            return jsonify({"error": "No comments provided"}), 400

        # Preprocess comments
        preprocessed_comments = [preprocess_comment(comment) for comment in comments]

        # Combine all comments into a single string
        text = ' '.join(preprocessed_comments)
        
        if not text.strip():
            return jsonify({"error": "No valid text found after preprocessing"}), 400

        # Generate the word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='#1e1e1e',
            colormap='Blues',
            stopwords=set(stopwords.words('english')),
            collocations=False,
            max_words=100
        ).generate(text)

        # Save the word cloud to a BytesIO object
        img_io = io.BytesIO()
        wordcloud.to_image().save(img_io, format='PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"Error in /generate_wordcloud: {e}")
        return jsonify({"error": f"Word cloud generation failed: {str(e)}"}), 500

@app.route('/generate_trend_graph', methods=['POST'])
def generate_trend_graph():
    try:
        data = request.get_json()
        sentiment_data = data.get('sentiment_data')

        if not sentiment_data:
            return jsonify({"error": "No sentiment data provided"}), 400

        # Convert sentiment data to DataFrame for easier processing
        df = pd.DataFrame(sentiment_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Calculate rolling average for smoother trend
        window_size = max(5, len(df) // 20)  # Adaptive window size
        df['rolling_avg'] = df['sentiment'].rolling(window=window_size, center=True).mean()

        # Generate the trend graph
        plt.figure(figsize=(12, 6))
        
        # Plot the rolling average
        plt.plot(df['timestamp'], df['rolling_avg'], color='#0099ff', linewidth=2, label='Sentiment Trend')
        
        # Plot individual sentiment points with colors
        colors = {1: '#4caf50', 0: '#9e9e9e', -1: '#ff6b6b'}
        for sentiment_val in [1, 0, -1]:
            mask = df['sentiment'] == sentiment_val
            plt.scatter(
                df[mask]['timestamp'],
                df[mask]['sentiment'],
                c=colors[sentiment_val],
                alpha=0.3,
                s=20,
                label=f"{'Positive' if sentiment_val == 1 else 'Neutral' if sentiment_val == 0 else 'Negative'}"
            )
        
        # Formatting
        plt.xlabel('Time', color='#f1f1f1', fontsize=12)
        plt.ylabel('Sentiment Score', color='#f1f1f1', fontsize=12)
        plt.title('Sentiment Trend Over Time', color='#f1f1f1', fontsize=14)
        plt.legend(loc='best', facecolor='#2a2a2a', edgecolor='#0099ff', labelcolor='#f1f1f1')
        plt.xticks(rotation=45, color='#f1f1f1')
        plt.yticks([-1, 0, 1], ['Negative', 'Neutral', 'Positive'], color='#f1f1f1')
        plt.grid(True, alpha=0.2, color='#555555')
        
        # Set background color
        plt.gca().set_facecolor('#1e1e1e')
        plt.gcf().patch.set_facecolor('#1e1e1e')
        plt.tight_layout()

        # Save the chart to a BytesIO object
        img_io = io.BytesIO()
        plt.savefig(img_io, format='PNG', facecolor='#1e1e1e', edgecolor='none', bbox_inches='tight')
        img_io.seek(0)
        plt.close()

        return send_file(img_io, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"Error in /generate_trend_graph: {e}")
        return jsonify({"error": f"Trend graph generation failed: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("YouTube Sentiment Analysis API - Simplified Version")
    print("="*60)
    print("Starting Flask app on http://0.0.0.0:5005")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5005, debug=True)
