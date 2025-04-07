import sys
import os
import json
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_predict_valid():
    with app.test_client() as client:
        with patch('app.requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"prediction": "Software"}

            response = client.post('/predict', json={"text": "Need access to VPN"})
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "prediction" in data

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