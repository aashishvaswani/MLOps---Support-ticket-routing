from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

# Load model and vectorizer
model = joblib.load('ticket_classification_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')
labels = [
    'Access', 'Administrative rights', 'HR Support', 'Hardware',
    'Internal Project', 'Miscellaneous', 'Purchase', 'Storage'
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    print(f">>> Request method: {request.method}")

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    print(">>> Received POST:", data)

    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    pred = model.predict(vectorized)[0]
    return jsonify({'prediction': labels[pred]}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
