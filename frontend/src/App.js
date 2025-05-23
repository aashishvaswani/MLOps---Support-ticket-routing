import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [trueLabel, setTrueLabel] = useState('');
  const [feedbackMsg, setFeedbackMsg] = useState('');

  const departments = [
    'Access',
    'Administrative rights',
    'HR Support',
    'Hardware',
    'Internal Project',
    'Miscellaneous',
    'Purchase',
    'Storage'
  ];

  const handlePredict = async () => {
    setLoading(true);
    setPrediction(null);
    setShowFeedbackForm(false);
    setFeedbackMsg('');
    try {
      const api = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      const res = await axios.post(`${api}/predict`, { text });
      setPrediction(res.data.prediction);
    } catch (err) {
      setPrediction(`Error: ${err.message}`);
    }
    setLoading(false);
  };

  const handleFeedback = async () => {
    try {
      const api = process.env.REACT_APP_API_URL || 'http://spe-backend.com';
      const res = await axios.post(`${api}/feedback`, {
        text,
        prediction,
        true_label: trueLabel
      });
      setFeedbackMsg(res.data.message);
      setTimeout(() => window.location.reload(), 1000);  // refresh after success
    } catch (err) {
      setFeedbackMsg(`Error: ${err.message}`);
    }
  };

  const handleYes = async () => {
    try {
      const api = process.env.REACT_APP_API_URL || 'http://localhost:5000';
      await axios.post(`${api}/feedback`, {
        text,
        prediction,
        true_label: prediction
      });
      window.location.reload();  // refresh on "Yes"
    } catch (err) {
      console.error('Feedback yes failed:', err.message);
    }
  };

  const handleNo = () => {
    setShowFeedbackForm(true);
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
        <div className="result-block">
          <div className="result">
            <strong>Prediction:</strong> {prediction}
          </div>

          <div className="feedback-buttons">
            <span>Was this prediction correct?</span>
            <button className="yes" onClick={handleYes}>Yes</button>
            <button className="no" onClick={handleNo}>No</button>
          </div>

          {showFeedbackForm && (
            <div className="feedback-form">
              <select
                value={trueLabel}
                onChange={(e) => setTrueLabel(e.target.value)}
              >
                <option value="">-- Select correct label --</option>
                {departments.map((dept) => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </select>
              <button onClick={handleFeedback}>Submit Feedback</button>
              {feedbackMsg && <p className="feedback-msg">{feedbackMsg}</p>}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
