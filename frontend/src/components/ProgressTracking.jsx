import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getProgressAnalysis, getUserAssessments, createProgressRecord } from '../services/api';

const ProgressTracking = ({ userId }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [showProgressForm, setShowProgressForm] = useState(false);
  const [progressForm, setProgressForm] = useState({
    weekly_score: 50,
    user_notes: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const analysis = await getProgressAnalysis(userId);
        setProgressData(analysis);

        // Prepare chart data from assessments
        const assessments = await getUserAssessments(userId);
        const chartDataPoints = assessments
          .slice()
          .reverse()
          .map((assessment, idx) => ({
            week: `Week ${idx + 1}`,
            score: assessment.burnout_score,
            date: new Date(assessment.created_at).toLocaleDateString(),
          }));
        setChartData(chartDataPoints);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to load progress data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userId]);

  const handleSubmitProgress = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await createProgressRecord({
        user_id: parseInt(userId),
        weekly_score: parseFloat(progressForm.weekly_score),
        user_notes: progressForm.user_notes || null,
      });

      // Refresh data
      const analysis = await getProgressAnalysis(userId);
      setProgressData(analysis);
      setShowProgressForm(false);
      setProgressForm({ weekly_score: 50, user_notes: '' });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save progress');
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving':
        return '📈';
      case 'declining':
        return '📉';
      case 'stagnant':
        return '➡️';
      default:
        return '📊';
    }
  };

  const getTrendClass = (trend) => {
    switch (trend) {
      case 'improving':
        return 'alert-success';
      case 'declining':
        return 'alert-danger';
      case 'stagnant':
        return 'alert-warning';
      default:
        return 'alert-info';
    }
  };

  if (loading && !progressData) {
    return (
      <div className="card">
        <div className="spinner"></div>
        <p style={{ textAlign: 'center' }}>Loading progress data...</p>
      </div>
    );
  }

  if (!progressData) {
    return (
      <div className="card">
        <h2>Progress Tracking</h2>
        <div className="alert alert-info">
          <p>No progress data available. Please complete an assessment first.</p>
        </div>
        <Link to="/assessment" className="btn btn-primary">
          Take Assessment
        </Link>
      </div>
    );
  }

  const { current_score, current_stage, progress_analysis, progress_history } = progressData;

  return (
    <div>
      <div className="card">
        <h2>Progress Tracking</h2>

        {error && <div className="alert alert-danger">{error}</div>}

        <div style={{ marginTop: '2rem' }}>
          <h3>Current Status</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ padding: '1rem', background: '#f8f9fa', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666' }}>Current Score</div>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3498db' }}>
                {current_score.toFixed(1)}
              </div>
            </div>
            <div style={{ padding: '1rem', background: '#f8f9fa', borderRadius: '6px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666' }}>Burnout Stage</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#2c3e50' }}>
                {current_stage}
              </div>
            </div>
          </div>
        </div>

        {progress_analysis && (
          <div style={{ marginTop: '2rem' }}>
            <h3>Progress Analysis</h3>
            <div className={`alert ${getTrendClass(progress_analysis.trend)}`} style={{ marginTop: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '1.5rem' }}>{getTrendIcon(progress_analysis.trend)}</span>
                <strong>Trend: {progress_analysis.trend.charAt(0).toUpperCase() + progress_analysis.trend.slice(1)}</strong>
              </div>
              {progress_analysis.change !== 0 && (
                <p>
                  Score change: {progress_analysis.change > 0 ? '+' : ''}
                  {progress_analysis.change.toFixed(1)} points
                </p>
              )}
              <p style={{ marginTop: '0.5rem' }}>{progress_analysis.recommendation}</p>
            </div>
          </div>
        )}

        <div style={{ marginTop: '2rem' }}>
          <h3>Burnout Score History</h3>
          {chartData.length > 0 ? (
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis domain={[0, 100]} label={{ value: 'Burnout Score', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#3498db"
                    strokeWidth={2}
                    name="Burnout Score"
                    dot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div className="alert alert-info" style={{ marginTop: '1rem' }}>
              <p>Not enough data points yet. Complete more assessments to see your progress over time.</p>
            </div>
          )}
        </div>

        {progress_history && progress_history.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h3>Progress Records</h3>
            <div style={{ marginTop: '1rem' }}>
              {progress_history.map((record) => (
                <div
                  key={record.progress_id}
                  style={{
                    padding: '1rem',
                    marginBottom: '0.5rem',
                    background: '#f8f9fa',
                    borderRadius: '6px',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <strong>Score: {record.weekly_score.toFixed(1)}</strong>
                      <div style={{ fontSize: '0.875rem', color: '#666', marginTop: '0.25rem' }}>
                        {new Date(record.timestamp).toLocaleDateString()}
                      </div>
                      {record.user_notes && (
                        <div style={{ marginTop: '0.5rem', fontStyle: 'italic' }}>
                          {record.user_notes}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ marginTop: '2rem' }}>
          {!showProgressForm ? (
            <button
              onClick={() => setShowProgressForm(true)}
              className="btn btn-primary"
            >
              Add Progress Record
            </button>
          ) : (
            <div className="card" style={{ marginTop: '1rem' }}>
              <h3>Add Progress Record</h3>
              <form onSubmit={handleSubmitProgress}>
                <div className="form-group">
                  <label htmlFor="weekly_score">
                    Weekly Score: {progressForm.weekly_score}
                  </label>
                  <input
                    type="range"
                    id="weekly_score"
                    min="0"
                    max="100"
                    value={progressForm.weekly_score}
                    onChange={(e) => setProgressForm({ ...progressForm, weekly_score: e.target.value })}
                    className="range-input"
                    required
                  />
                  <div className="range-labels">
                    <span>0 (Healthy)</span>
                    <span>50 (Moderate)</span>
                    <span>100 (Severe)</span>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="user_notes">Notes (Optional)</label>
                  <textarea
                    id="user_notes"
                    value={progressForm.user_notes}
                    onChange={(e) => setProgressForm({ ...progressForm, user_notes: e.target.value })}
                    rows="3"
                    style={{
                      width: '100%',
                      padding: '0.75rem',
                      border: '1px solid #ddd',
                      borderRadius: '6px',
                      fontSize: '1rem',
                      fontFamily: 'inherit',
                    }}
                  />
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Progress'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowProgressForm(false);
                      setProgressForm({ weekly_score: 50, user_notes: '' });
                    }}
                    className="btn btn-secondary"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>

        <div style={{ marginTop: '2rem' }}>
          <Link to="/assessment" className="btn btn-secondary">
            Take New Assessment
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ProgressTracking;
