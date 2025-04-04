import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    console.log("Sending text:", text);

    try {
      const api = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const res = await axios.post(`${api}/predict`, { text });
      console.log("Response from backend:", res.data);
      setPrediction(res.data.prediction);
    } catch (err) {
      console.error("Request failed:", err);
      setPrediction(`Error: ${err.message}`);
    }

    setLoading(false);
  };

  return (
    <div className="App" style={{ padding: '2rem' }}>
      <h1>🎫 IT Service Ticket Classifier</h1>
      <textarea
        rows="5"
        cols="60"
        placeholder="Describe your issue..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ padding: '1rem', fontSize: '1rem' }}
      />
      <br /><br />
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Submit'}
      </button>
      <br /><br />
      {prediction && (
        <div>
          <strong>Prediction:</strong> {prediction}
        </div>
      )}
    </div>
  );
}

export default App;
