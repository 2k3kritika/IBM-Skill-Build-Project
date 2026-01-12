import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getAssessmentDetails, generateRecoveryPlan } from '../services/api';

const ResultPage = ({ userId }) => {
  const { assessmentId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [assessmentDetails, setAssessmentDetails] = useState(null);
  const [generatingPlan, setGeneratingPlan] = useState(false);

  useEffect(() => {
    const fetchAssessmentDetails = async () => {
      try {
        const details = await getAssessmentDetails(assessmentId);
        setAssessmentDetails(details);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load assessment details');
      } finally {
        setLoading(false);
      }
    };

    fetchAssessmentDetails();
  }, [assessmentId]);

  const handleGeneratePlan = async () => {
    if (!userId) {
      setError('User ID not found');
      return;
    }

    setGeneratingPlan(true);
    setError(null);

    try {
      const plan = await generateRecoveryPlan({
        user_id: parseInt(userId),
        assessment_id: parseInt(assessmentId),
      });
      navigate('/recovery');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate recovery plan');
    } finally {
      setGeneratingPlan(false);
    }
  };

  const getScoreClass = (score) => {
    if (score <= 25) return 'score-healthy';
    if (score <= 50) return 'score-early';
    if (score <= 75) return 'score-moderate';
    return 'score-severe';
  };

  const getStageClass = (stage) => {
    const stageLower = stage.toLowerCase();
    if (stageLower.includes('healthy')) return 'alert-success';
    if (stageLower.includes('early')) return 'alert-warning';
    if (stageLower.includes('moderate')) return 'alert-warning';
    if (stageLower.includes('severe')) return 'alert-danger';
    return 'alert-info';
  };

  if (loading) {
    return (
      <div className="card">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading assessment results...</p>
      </div>
    );
  }

  if (error && !assessmentDetails) {
    return (
      <div className="card">
        <div className="alert alert-danger">{error}</div>
        <Link to="/assessment" className="btn btn-secondary">
          Back to Assessment
        </Link>
      </div>
    );
  }

  if (!assessmentDetails) {
    return null;
  }

  const { burnout_score, burnout_stage, classification, explanation, score_breakdown } = assessmentDetails;

  return (
    <div>
      <div className="card">
        <h2>Your Burnout Assessment Results</h2>

        <div className="score-display">
          <div className={`score-value ${getScoreClass(burnout_score)}`}>
            {burnout_score.toFixed(1)}
          </div>
          <p style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Burnout Score (out of 100)</p>
        </div>

        <div className={`alert ${getStageClass(burnout_stage)}`}>
          <h3 style={{ marginBottom: '0.5rem' }}>Burnout Stage: {burnout_stage}</h3>
          <p>{classification.description}</p>
        </div>

        <div className="alert alert-info" style={{ marginTop: '2rem' }}>
          <strong>Explanation:</strong> {explanation}
        </div>

        <div style={{ marginTop: '2rem' }}>
          <h3>Score Breakdown</h3>
          <div style={{ marginTop: '1rem' }}>
            {Object.entries(score_breakdown).map(([factor, value]) => (
              <div key={factor} style={{ marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span style={{ textTransform: 'capitalize' }}>
                    {factor.replace(/_/g, ' ')}:
                  </span>
                  <span style={{ fontWeight: 'bold' }}>{value}%</span>
                </div>
                <div
                  style={{
                    width: '100%',
                    height: '8px',
                    backgroundColor: '#e0e0e0',
                    borderRadius: '4px',
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      width: `${value}%`,
                      height: '100%',
                      backgroundColor: value > 20 ? '#e74c3c' : value > 10 ? '#f39c12' : '#27ae60',
                      transition: 'width 0.3s',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="alert alert-warning" style={{ marginTop: '2rem' }}>
          <strong>Disclaimer:</strong> This assessment is not a medical diagnosis. It is a
          decision-support tool for awareness purposes only. If you are experiencing severe
          symptoms, please consult a healthcare professional.
        </div>

        {error && <div className="alert alert-danger" style={{ marginTop: '1rem' }}>{error}</div>}

        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem' }}>
          <button
            onClick={handleGeneratePlan}
            className="btn btn-primary"
            disabled={generatingPlan || !userId}
          >
            {generatingPlan ? 'Generating Plan...' : 'Generate Recovery Plan'}
          </button>
          <Link to="/assessment" className="btn btn-secondary">
            Take Assessment Again
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;
