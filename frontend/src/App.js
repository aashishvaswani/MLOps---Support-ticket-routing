import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const api = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const res = await axios.post(`${api}/predict`, { text });
      setPrediction(res.data.prediction);
    } catch (err) {
      setPrediction(`Error: ${err.message}`);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>🎫 IT Ticket Classifier</h1>
      <textarea
        placeholder="Describe your issue..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Submit'}
      </button>
      {prediction && (
        <div className="result">
          <strong>Prediction:</strong> {prediction}
        </div>
      )}
    </div>
  );
}

export default App;
