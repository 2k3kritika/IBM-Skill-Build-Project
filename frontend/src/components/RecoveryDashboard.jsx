import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getLatestRecoveryPlan, generateRecoveryPlan, getUserAssessments } from '../services/api';

const RecoveryDashboard = ({ userId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [recoveryPlan, setRecoveryPlan] = useState(null);
  const [completionStatus, setCompletionStatus] = useState({});
  const [hasAssessment, setHasAssessment] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Check if user has assessments
        const assessments = await getUserAssessments(userId);
        setHasAssessment(assessments.length > 0);

        if (assessments.length > 0) {
          // Try to get latest recovery plan
          try {
            const plan = await getLatestRecoveryPlan(userId);
            setRecoveryPlan(plan);
            if (plan.recommendations.completion_status) {
              setCompletionStatus(plan.recommendations.completion_status);
            }
          } catch (err) {
            // No recovery plan exists yet
            if (err.response?.status === 404) {
              setError('No recovery plan found. Please complete an assessment first.');
            } else {
              setError(err.response?.data?.detail || 'Failed to load recovery plan');
            }
          }
        }
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userId]);

  const handleGeneratePlan = async () => {
    setLoading(true);
    setError(null);

    try {
      const assessments = await getUserAssessments(userId);
      if (assessments.length === 0) {
        setError('Please complete an assessment first.');
        setLoading(false);
        return;
      }

      const latestAssessment = assessments[0];
      const plan = await generateRecoveryPlan({
        user_id: parseInt(userId),
        assessment_id: latestAssessment.assessment_id,
      });

      setRecoveryPlan(plan);
      if (plan.recommendations.completion_status) {
        setCompletionStatus(plan.recommendations.completion_status);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate recovery plan');
    } finally {
      setLoading(false);
    }
  };

  const toggleCompletion = (category, index) => {
    const key = `${category}_${index}`;
    setCompletionStatus((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  if (loading) {
    return (
      <div className="card">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading recovery plan...</p>
      </div>
    );
  }

  if (!hasAssessment) {
    return (
      <div className="card">
        <h2>Recovery Plan Dashboard</h2>
        <div className="alert alert-info">
          <p>Please complete an assessment first to generate a personalized recovery plan.</p>
        </div>
        <Link to="/assessment" className="btn btn-primary">
          Take Assessment
        </Link>
      </div>
    );
  }

  if (!recoveryPlan) {
    return (
      <div className="card">
        <h2>Recovery Plan Dashboard</h2>
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="alert alert-info">
          <p>No recovery plan found. Generate one based on your latest assessment.</p>
        </div>
        <button onClick={handleGeneratePlan} className="btn btn-primary" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Recovery Plan'}
        </button>
      </div>
    );
  }

  const recommendations = recoveryPlan.recommendations;

  return (
    <div>
      <div className="card">
        <h2>Your Personalized Recovery Plan</h2>
        <p style={{ color: '#666', marginBottom: '2rem' }}>
          Generated on {new Date(recoveryPlan.created_at).toLocaleDateString()}
        </p>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="alert alert-warning">
          <strong>Disclaimer:</strong> {recommendations.disclaimer || 'This is not medical advice. Please consult a healthcare professional for severe symptoms.'}
        </div>

        {recommendations.caution_notes && recommendations.caution_notes.length > 0 && (
          <div className="alert alert-danger" style={{ marginTop: '1rem' }}>
            <strong>Important Notes:</strong>
            <ul style={{ marginTop: '0.5rem', marginLeft: '1.5rem' }}>
              {recommendations.caution_notes.map((note, idx) => (
                <li key={idx}>{note}</li>
              ))}
            </ul>
          </div>
        )}

        <div style={{ marginTop: '2rem' }}>
          <h3>Daily Actions</h3>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Small, achievable micro-actions you can take each day:
          </p>
          <ul className="checklist">
            {recommendations.daily_actions?.map((action, idx) => {
              const key = `daily_${idx}`;
              const completed = completionStatus[key] || false;
              return (
                <li key={idx} className={`checklist-item ${completed ? 'completed' : ''}`}>
                  <input
                    type="checkbox"
                    checked={completed}
                    onChange={() => toggleCompletion('daily', idx)}
                  />
                  <span>{action}</span>
                </li>
              );
            })}
          </ul>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h3>Weekly Goals</h3>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Broader recovery objectives for the week:
          </p>
          <ul className="checklist">
            {recommendations.weekly_goals?.map((goal, idx) => {
              const key = `weekly_${idx}`;
              const completed = completionStatus[key] || false;
              return (
                <li key={idx} className={`checklist-item ${completed ? 'completed' : ''}`}>
                  <input
                    type="checkbox"
                    checked={completed}
                    onChange={() => toggleCompletion('weekly', idx)}
                  />
                  <span>{goal}</span>
                </li>
              );
            })}
          </ul>
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h3>Behavioral Suggestions</h3>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Lifestyle adjustments to support recovery:
          </p>
          <ul style={{ listStyle: 'disc', marginLeft: '2rem' }}>
            {recommendations.behavioral_suggestions?.map((suggestion, idx) => (
              <li key={idx} style={{ marginBottom: '0.5rem' }}>{suggestion}</li>
            ))}
          </ul>
        </div>

        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
          <button onClick={handleGeneratePlan} className="btn btn-secondary" disabled={loading}>
            {loading ? 'Regenerating...' : 'Regenerate Plan'}
          </button>
          <Link to="/progress" className="btn btn-primary">
            View Progress
          </Link>
        </div>
      </div>
    </div>
  );
};

export default RecoveryDashboard;
