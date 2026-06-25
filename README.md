# 🎯 Advanced Sentiment Analysis System

A modern web-based sentiment analysis tool that uses machine learning to classify text reviews as **Positive**, **Negative**, or **Neutral** with confidence scores.

## ✨ Features

- 🤖 **ML-Powered Analysis**: Uses Random Forest Classifier with TF-IDF vectorization
- 📊 **Real-time Results**: Get instant sentiment predictions with confidence scores
- 💾 **Analysis History**: Track your recent analyses
- 📈 **Performance Metrics**: Accuracy, Precision, Recall, and F1-Score
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🔗 **REST API**: JSON endpoints for programmatic access

## 🏗️ Project Structure

```
sentiment-analysis/
├── app.py                    # Flask web server
├── model.py                  # ML model training script
├── requirements.txt          # Python dependencies
├── sentiment_model.pkl       # Trained model (generated)
├── vectorizer.pkl           # TF-IDF vectorizer (generated)
├── README.md                # This file
├── dataset/
│   └── IMDB Dataset.csv     # Training dataset (download required)
└── templates/
    └── index.html           # Web UI
```

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/simicheriyan16/sentiment-analysis.git
cd sentiment-analysis
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Dataset
Download the IMDB Dataset from [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) and place it in a `dataset` folder:

```
sentiment-analysis/
└── dataset/
    └── IMDB Dataset.csv
```

### Step 5: Train the Model
```bash
python model.py
```

Expected output:
```
============================================================
🤖 SENTIMENT ANALYSIS MODEL TRAINING
============================================================
📚 Loading dataset...
✅ Dataset loaded successfully!
📊 Total Reviews: 50000
...
✅ Model trained and saved successfully!
📁 Generated files:
   ✓ sentiment_model.pkl
   ✓ vectorizer.pkl
```

### Step 6: Run the Web Server
```bash
python app.py
```

Open your browser and go to: **http://localhost:5000**

## 🔧 How It Works

### Backend (Python + scikit-learn)

1. **Data Preprocessing**: Removes stop words and normalizes text
2. **Feature Extraction**: TF-IDF vectorization with bigrams
3. **Model Training**: Random Forest Classifier with 100 estimators
4. **Prediction**: Classifies new reviews with confidence scores

### Model Specifications

- **Algorithm**: Random Forest Classifier
- **Features**: 5,000 TF-IDF features with bigrams
- **Training/Testing**: 80/20 split
- **Cross-validation**: Stratified to maintain class distribution

### Frontend (HTML + Jinja2 Templates)

- Real-time form submission
- Dynamic result display with emoji indicators
- Analysis history tracking
- Responsive mobile-friendly design

## 📊 API Endpoints

### GET `/`
Web interface for sentiment analysis

### POST `/api/analyze`
Analyze sentiment via JSON API

**Request:**
```json
{
    "text": "This product is absolutely amazing!"
}
```

**Response:**
```json
{
    "sentiment": "positive",
    "label": "😊 Positive",
    "emoji": "😊",
    "confidence": 92.45,
    "probabilities": {
        "positive": 92.45,
        "negative": 7.55
    }
}
```

### GET `/history`
Get recent analysis history (last 20 items)

### GET `/stats`
Get overall statistics

**Response:**
```json
{
    "total": 42,
    "positive": 28,
    "negative": 14,
    "average_confidence": 87.35
}
```

## 📈 Model Performance

After training on IMDB dataset:

| Metric | Score |
|--------|-------|
| Accuracy | ~89% |
| Precision | ~89% |
| Recall | ~89% |
| F1-Score | ~89% |

*Scores vary based on dataset size and model configuration*

## 💡 Example Usage

**Input**: "I absolutely loved this! Best experience ever!"
**Output**:
- Sentiment: **Positive** 😊
- Confidence: **94.32%**
- Review Length: 42 characters

**Input**: "Terrible product. Wasted my money."
**Output**:
- Sentiment: **Negative** 😞
- Confidence: **88.75%**
- Review Length: 34 characters

## 🔐 Security Notes

- Input validation: Minimum 5 characters
- HTML escaping: Jinja2 auto-escapes by default
- CSRF protection: Use Flask-WTF for production
- Rate limiting: Add Flask-Limiter for production

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: sentiment_model.pkl not found` | Run `python model.py` to train the model |
| `Port 5000 already in use` | Change to different port: `app.run(port=5001)` |
| `pandas.errors.ParserError` | Ensure CSV is in correct format or download fresh dataset |

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Real-time model retraining
- [ ] Database integration for persistent history
- [ ] Emotion detection (joy, anger, sadness, etc.)
- [ ] Aspect-based sentiment analysis
- [ ] User authentication & profiles
- [ ] Export results as PDF/CSV
- [ ] Deployment on Heroku/AWS
- [ ] WebSocket for live updates

## 📚 Dependencies

- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data processing
- **numpy** - Numerical computing

## 📝 License

MIT License - Feel free to use this project for educational and commercial purposes!

## 🤝 Contributing

Found a bug? Have an idea? Create an issue or submit a pull request!

## 📞 Support

For questions or issues, please create an issue on GitHub.

---

**Made with ❤️ for ML enthusiasts**

Start analyzing sentiments today! 🚀
