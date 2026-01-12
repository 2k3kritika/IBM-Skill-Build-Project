import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import AssessmentForm from './components/AssessmentForm';
import ResultPage from './components/ResultPage';
import RecoveryDashboard from './components/RecoveryDashboard';
import ProgressTracking from './components/ProgressTracking';

function App() {
  const [userId, setUserId] = useState(() => {
    return localStorage.getItem('userId');
  });

  useEffect(() => {
    if (userId) {
      localStorage.setItem('userId', userId);
    } else {
      localStorage.removeItem('userId');
    }
  }, [userId]);

  return (
    <Router>
      <div className="App">
        <nav>
          <div className="container">
            <ul>
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/assessment">Assessment</Link>
              </li>
              {userId && (
                <>
                  <li>
                    <Link to="/recovery">Recovery Plan</Link>
                  </li>
                  <li>
                    <Link to="/progress">Progress</Link>
                  </li>
                </>
              )}
            </ul>
          </div>
        </nav>

        <div className="container">
          <Routes>
            <Route
              path="/"
              element={
                <div className="card">
                  <h1>AI-Powered Burnout Detection and Recovery Planning</h1>
                  <p style={{ marginTop: '1rem', lineHeight: '1.6' }}>
                    Welcome to the Burnout Detection and Recovery Planning system. This tool helps you
                    assess your burnout levels and provides personalized recovery recommendations.
                  </p>
                  <div className="alert alert-info" style={{ marginTop: '2rem' }}>
                    <strong>Important:</strong> This system is NOT a medical diagnostic tool. It serves
                    as a decision-support and awareness tool only. Please consult a healthcare professional
                    for medical advice.
                  </div>
                  <div style={{ marginTop: '2rem' }}>
                    <Link to="/assessment" className="btn btn-primary">
                      Start Assessment
                    </Link>
                  </div>
                </div>
              }
            />
            <Route
              path="/assessment"
              element={
                <AssessmentForm
                  userId={userId}
                  setUserId={setUserId}
                />
              }
            />
            <Route
              path="/result/:assessmentId"
              element={<ResultPage userId={userId} />}
            />
            <Route
              path="/recovery"
              element={
                userId ? (
                  <RecoveryDashboard userId={userId} />
                ) : (
                  <Navigate to="/assessment" replace />
                )
              }
            />
            <Route
              path="/progress"
              element={
                userId ? (
                  <ProgressTracking userId={userId} />
                ) : (
                  <Navigate to="/assessment" replace />
                )
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
