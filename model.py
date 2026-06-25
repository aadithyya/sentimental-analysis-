import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

# Shared cleaning function - the SAME function is used later in app.py,
# so training and live predictions always see text in the same shape.
from text_utils import clean_text

print("=" * 60)
print("🤖 SENTIMENT ANALYSIS MODEL TRAINING")
print("=" * 60)

print("\n📚 Loading dataset...")

# Load dataset
try:
    data = pd.read_csv("dataset/IMDB Dataset.csv")
    print(f"✅ Dataset loaded successfully!")
    print(f"📊 Total Reviews: {len(data)}")
    print(f"📝 Columns: {list(data.columns)}")
except FileNotFoundError:
    print("❌ Error: Dataset not found. Please place 'IMDB Dataset.csv' in 'dataset' folder")
    exit()

# --- Clean the review text before doing anything else with it ---
# Raw IMDB reviews are full of "<br /><br />" HTML line breaks, punctuation,
# and mixed casing. clean_text() strips all of that down to plain lowercase
# words, so the vectorizer spends its limited vocabulary on real words
# instead of HTML noise like "br".
print("\n🧹 Cleaning review text (removing HTML tags, punctuation, etc.)...")
data["review"] = data["review"].apply(clean_text)

# Features and Labels
X = data["review"]
y = data["sentiment"]

print(f"\n📈 Sentiment Distribution:")
print(y.value_counts())

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\n✂️ Data Split:")
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")

print(f"\n🔄 Vectorizing text...")

# Convert text to numerical features using TF-IDF.
# sublinear_tf=True dampens the score of words that repeat MANY times in a
# single review (e.g. "good good good good") - a small, free accuracy boost
# for this kind of text classification, with no extra dependency required.
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.8,
    sublinear_tf=True
)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

print(f"✅ Vectorization complete!")
print(f"   Feature matrix shape: {X_train_vectorized.shape}")

print(f"\n🧠 Training model...")

# Train model using Random Forest.
# - n_estimators is a bit higher and max_depth is no longer capped, which
#   tends to improve accuracy on TF-IDF text features.
# - class_weight='balanced' keeps the model robust even if one sentiment
#   ends up slightly more common than the other.
# None of this affects how light the running WEB APP is - it's a one-off
# cost paid only when training, not every time someone analyzes a review.
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=None,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

model.fit(X_train_vectorized, y_train)

print(f"\n🧪 Testing model...")

# Predict
predictions = model.predict(X_test_vectorized)

# Evaluation metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')
recall = recall_score(y_test, predictions, average='weighted')
f1 = f1_score(y_test, predictions, average='weighted')

print(f"\n📊 MODEL PERFORMANCE METRICS:")
print(f"   Accuracy:  {accuracy * 100:.2f}%")
print(f"   Precision: {precision * 100:.2f}%")
print(f"   Recall:    {recall * 100:.2f}%")
print(f"   F1 Score:  {f1 * 100:.2f}%")

# Save trained files
pickle.dump(model, open("sentiment_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print(f"\n✅ Model trained and saved successfully!")
print(f"📁 Generated files:")
print(f"   ✓ sentiment_model.pkl")
print(f"   ✓ vectorizer.pkl")
print(f"\n{'=' * 60}")
print("Ready to use! Run 'python app.py' to start the web server.")
print(f"{'=' * 60}\n")