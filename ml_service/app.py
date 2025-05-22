from flask import Flask, request, jsonify
import joblib
import re
import os
import time
from threading import Thread

app = Flask(__name__)

MODEL_PATH = "/shared-model/ticket_classification_model.pkl"
VECTORIZER_PATH = "/shared-model/tfidf_vectorizer.pkl"

labels = [
    'Access', 'Administrative rights', 'HR Support', 'Hardware',
    'Internal Project', 'Miscellaneous', 'Purchase', 'Storage'
]

model = None
vectorizer = None
last_modified = None

def load_model():
    global model, vectorizer, last_modified
    print("🔁 Loading model...")
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    last_modified = os.path.getmtime(MODEL_PATH)

def watch_model(interval=10):
    global last_modified
    while True:
        try:
            current_mod = os.path.getmtime(MODEL_PATH)
            if current_mod != last_modified:
                print("📦 Model updated — reloading...")
                load_model()
        except Exception as e:
            print(f"⚠️ Watcher error: {e}")
        time.sleep(interval)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        cleaned = clean_text(text)
        vectorized = vectorizer.transform([cleaned])
        pred = model.predict(vectorized)[0]

        # 🔁 Convert to int if needed
        if hasattr(pred, 'item'):
            pred = pred.item()

        return jsonify({'prediction': labels[pred]})

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    load_model()
    Thread(target=watch_model, daemon=True).start()
    app.run(host='0.0.0.0', port=6000)
