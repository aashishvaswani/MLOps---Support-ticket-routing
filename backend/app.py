from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from logger_config import setup_logger
import joblib
import re
import time  # for latency tracking
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Setup logger
logger = setup_logger()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, 'ticket_classification_model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'tfidf_vectorizer.pkl')

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

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
    start_time = time.time()

    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    text = data.get('text', '')

    logger.info("Request received", extra={
        "endpoint": "/predict",
        "method": request.method,
        "prediction": None,
        "input": text or None
    })

    logger.info("Input received", extra={
        "endpoint": "/predict",
        "method": "POST",
        "prediction": None,
        "input": text or None
    })

    if not text:
        logger.warning("No text provided", extra={
            "endpoint": "/predict",
            "method": "POST",
            "input": None,
            "latency_ms": int((time.time() - start_time) * 1000),
            "status_code": 400
        })
        return jsonify({'error': 'No text provided'}), 400

    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    pred = model.predict(vectorized)[0]

    latency_ms = int((time.time() - start_time) * 1000)
    status_code = 200

    logger.info("Prediction made", extra={
        "endpoint": "/predict",
        "prediction": labels[pred],
        "input": text or None,
        "method": "POST",
        "latency_ms": latency_ms,
        "status_code": status_code
    })

    return jsonify({'prediction': labels[pred]}), status_code

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
