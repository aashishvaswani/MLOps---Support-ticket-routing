from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from logger_config import setup_logger
import requests
import time

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Setup logger
logger = setup_logger()

ML_SERVICE_URL = "http://ml-service:6000/predict"

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

    if not text:
        logger.warning("No text provided", extra={
            "endpoint": "/predict",
            "method": "POST",
            "input": None,
            "latency_ms": int((time.time() - start_time) * 1000),
            "status_code": 400
        })
        return jsonify({'error': 'No text provided'}), 400

    try:
        response = requests.post(ML_SERVICE_URL, json={'text': text})
        response.raise_for_status()
        prediction = response.json()
        status_code = response.status_code
    except Exception as e:
        logger.error("ML service call failed", extra={
            "endpoint": "/predict",
            "input": text,
            "method": "POST",
            "error": str(e),
            "status_code": 500
        })
        return jsonify({'error': 'Failed to get prediction from ML service'}), 500

    latency_ms = int((time.time() - start_time) * 1000)

    logger.info("Prediction successful", extra={
        "endpoint": "/predict",
        "prediction": prediction.get('prediction'),
        "input": text,
        "method": "POST",
        "latency_ms": latency_ms,
        "status_code": status_code
    })

    return jsonify(prediction), status_code

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
