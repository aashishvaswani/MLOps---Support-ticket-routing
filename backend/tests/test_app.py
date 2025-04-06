import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, labels

def test_predict_valid():
    with app.test_client() as client:
        response = client.post('/predict', json={"text": "Need access to VPN"})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["prediction"] in labels

def test_predict_empty():
    with app.test_client() as client:
        response = client.post('/predict', json={"text": ""})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

def test_predict_missing_field():
    with app.test_client() as client:
        response = client.post('/predict', json={})
        assert response.status_code == 400

def test_options_method():
    with app.test_client() as client:
        response = client.open('/predict', method='OPTIONS')
        assert response.status_code == 200
