from flask import Flask, request, jsonify
import joblib
import re
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, 'ticket_classification_model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl'))

labels = [
    'Access', 'Administrative rights', 'HR Support', 'Hardware',
    'Internal Project', 'Miscellaneous', 'Purchase', 'Storage'
]

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
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    pred = model.predict(vectorized)[0]
    return jsonify({'prediction': labels[pred]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
