from flask import Flask, render_template, request, jsonify
import pickle
from datetime import datetime

# Same text-cleaning function used during training (model.py), so the
# model always sees prediction input in the same shape it learned from.
from text_utils import clean_text

app = Flask(__name__)

# Load trained model and vectorizer
try:
    model = pickle.load(open("sentiment_model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    print("✅ Model and vectorizer loaded successfully!")
except FileNotFoundError:
    print("❌ Error: Model files not found. Please run 'python model.py' first.")
    exit()

# Store analysis history in memory (fine for a student project - this
# resets whenever the server restarts; a real production app would save
# this to a database instead).
analysis_history = []

# Label/emoji shown for each sentiment the MODEL can actually predict.
# The IMDB dataset only contains "positive" and "negative" reviews, so
# that's the only thing the trained model ever learned to output - there
# is no "neutral" class.
SENTIMENT_MAP = {
    'positive': {'label': '😊 Positive', 'emoji': '😊'},
    'negative': {'label': '😞 Negative', 'emoji': '😞'},
}


def analyze_sentiment(review_text):
    """Clean the review, run it through the model, and return the result."""
    try:
        # Clean the text the SAME way it was cleaned during training.
        cleaned = clean_text(review_text)
        transformed_review = vectorizer.transform([cleaned])

        # Get prediction
        sentiment = model.predict(transformed_review)[0]

        # Get confidence scores
        probabilities = model.predict_proba(transformed_review)[0]
        confidence = max(probabilities) * 100

        sentiment_lower = sentiment.lower()
        result = SENTIMENT_MAP.get(sentiment_lower, {'label': sentiment, 'emoji': '🤔'})

        # IMPORTANT: scikit-learn orders the columns of predict_proba()
        # according to model.classes_, which is sorted ALPHABETICALLY -
        # not in the order "positive, negative". That means column 0 is
        # actually "negative" and column 1 is "positive". Looking the
        # index up by name (instead of assuming 0/1) keeps this correct
        # no matter what order scikit-learn happens to use.
        class_index = {cls.lower(): i for i, cls in enumerate(model.classes_)}
        positive_pct = probabilities[class_index['positive']] * 100 if 'positive' in class_index else 0
        negative_pct = probabilities[class_index['negative']] * 100 if 'negative' in class_index else 0

        return {
            'sentiment': sentiment,
            'label': result['label'],
            'emoji': result['emoji'],
            'confidence': round(confidence, 2),
            'probabilities': {
                'positive': round(positive_pct, 2),
                'negative': round(negative_pct, 2),
            }
        }
    except Exception as e:
        return {'error': str(e)}


@app.route("/", methods=["GET"])
def home():
    """
    Serve the page. All of the real analysis work now happens through
    /api/analyze, which the page's JavaScript calls with fetch() - so this
    route just needs to render the empty template. (Previously this route
    also handled form POSTs and re-rendered results with Jinja - that path
    is gone now that the frontend talks to the API directly.)
    """
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """API endpoint the frontend's JavaScript calls to analyze a review."""
    try:
        data = request.get_json(silent=True) or {}
        review_text = data.get('text', '').strip()

        if not review_text:
            return jsonify({'error': 'Review text is required'}), 400

        if len(review_text) < 5:
            return jsonify({'error': 'Review must be at least 5 characters'}), 400

        result = analyze_sentiment(review_text)

        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # Store in history
        analysis_history.append({
            'review': review_text[:50] + '...' if len(review_text) > 50 else review_text,
            'sentiment': result['sentiment'],
            'confidence': result['confidence'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/history", methods=["GET"])
def get_history():
    """Get recent analysis history, most recent first."""
    recent = analysis_history[-20:]
    return jsonify({'history': list(reversed(recent))})


@app.route("/stats", methods=["GET"])
def get_stats():
    """Get sentiment statistics"""
    if not analysis_history:
        return jsonify({
            'total': 0,
            'positive': 0,
            'negative': 0,
            'average_confidence': 0
        })

    sentiments = [h['sentiment'].lower() for h in analysis_history]
    positive_count = sentiments.count('positive')
    negative_count = sentiments.count('negative')
    avg_confidence = sum(h['confidence'] for h in analysis_history) / len(analysis_history)

    return jsonify({
        'total': len(analysis_history),
        'positive': positive_count,
        'negative': negative_count,
        'average_confidence': round(avg_confidence, 2)
    })


if __name__ == "__main__":
    print("🚀 Starting Sentiment Analysis Web Server...")
    print("📍 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)