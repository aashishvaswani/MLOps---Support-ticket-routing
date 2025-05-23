import pandas as pd
import re
import joblib
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from collections import Counter

# File paths
DATASET_PATH = "all_tickets_processed_improved_v3.csv"
MODEL_PATH = "/shared-model/ticket_classification_model.pkl"
VECTORIZER_PATH = "/shared-model/tfidf_vectorizer.pkl"

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

print(f"[{datetime.now()}] 📥 Loading dataset...")
df = pd.read_csv(DATASET_PATH)
df.dropna(inplace=True)

print(f"[{datetime.now()}] 🧹 Cleaning text...")
df['cleaned_document'] = df['Document'].apply(clean_text)

print(f"[{datetime.now()}] 🔢 TF-IDF vectorizing...")
tfidf = TfidfVectorizer(max_features=500)
X = tfidf.fit_transform(df['cleaned_document']).toarray()

print(f"[{datetime.now()}] 🏷️ Label encoding...")
le = LabelEncoder()
y = le.fit_transform(df['Topic_group'])

label_counts = Counter(y)
min_class_size = min(label_counts.values())
stratify_param = y if min_class_size >= 2 else None

print(f"[{datetime.now()}] 🔀 Splitting train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=stratify_param
)

print(f"[{datetime.now()}] 🤖 Training model...")
model = LogisticRegression(max_iter=500, solver='liblinear')
model.fit(X_train, y_train)

print(f"[{datetime.now()}] 📈 Evaluating model...")
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')
print(classification_report(y_test, y_pred, target_names=le.classes_))

print(f"[{datetime.now()}] 💾 Saving model and vectorizer...")
joblib.dump(model, MODEL_PATH)
joblib.dump(tfidf, VECTORIZER_PATH)
