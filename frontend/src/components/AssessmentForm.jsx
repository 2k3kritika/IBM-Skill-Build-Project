import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser, createAssessment } from '../services/api';

const AssessmentForm = ({ userId, setUserId }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(1);
  const [userData, setUserData] = useState({
    name: '',
    age_range: '18-25',
    occupation_type: 'student',
  });
  const [assessmentData, setAssessmentData] = useState({
    daily_work_hours: 8,
    sleep_duration: 7,
    sleep_quality: 3,
    emotional_exhaustion: 3,
    motivation_level: 3,
    screen_time: 3,
    perceived_stress: 3,
  });

  const handleUserSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const user = await createUser(userData);
      setUserId(user.user_id.toString());
      setStep(2);
    } catch (err) {
      console.error('Error creating user:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to create user';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleAssessmentSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const currentUserId = userId || localStorage.getItem('userId');
      if (!currentUserId) {
        setError('User ID not found. Please start over.');
        return;
      }

      const assessment = await createAssessment({
        user_id: parseInt(currentUserId),
        responses: assessmentData,
      });

      navigate(`/result/${assessment.assessment_id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit assessment');
    } finally {
      setLoading(false);
    }
  };

  const updateAssessmentValue = (field, value) => {
    setAssessmentData((prev) => ({
      ...prev,
      [field]: parseFloat(value) || value,
    }));
  };

  if (step === 1) {
    return (
      <div className="card">
        <h2>User Information</h2>
        <form onSubmit={handleUserSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name *</label>
            <input
              type="text"
              id="name"
              value={userData.name}
              onChange={(e) => setUserData({ ...userData, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="age_range">Age Range *</label>
            <select
              id="age_range"
              value={userData.age_range}
              onChange={(e) => setUserData({ ...userData, age_range: e.target.value })}
              required
            >
              <option value="18-25">18-25</option>
              <option value="26-35">26-35</option>
              <option value="36-45">36-45</option>
              <option value="46-55">46-55</option>
              <option value="56-65">56-65</option>
              <option value="65+">65+</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="occupation_type">Occupation Type *</label>
            <select
              id="occupation_type"
              value={userData.occupation_type}
              onChange={(e) => setUserData({ ...userData, occupation_type: e.target.value })}
              required
            >
              <option value="student">Student</option>
              <option value="professional">Professional</option>
              <option value="other">Other</option>
            </select>
          </div>

          {error && <div className="alert alert-danger">{error}</div>}

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Creating...' : 'Continue to Assessment'}
          </button>
        </form>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>Burnout Assessment</h2>
      <p style={{ marginBottom: '2rem', color: '#666' }}>
        Please answer the following questions honestly. All responses are confidential.
      </p>

      <form onSubmit={handleAssessmentSubmit}>
        <div className="form-group">
          <label htmlFor="daily_work_hours">
            Daily Work/Study Hours: {assessmentData.daily_work_hours} hours
          </label>
          <input
            type="range"
            id="daily_work_hours"
            min="0"
            max="16"
            step="0.5"
            value={assessmentData.daily_work_hours}
            onChange={(e) => updateAssessmentValue('daily_work_hours', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>0</span>
            <span>8 (Normal)</span>
            <span>16</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="sleep_duration">
            Sleep Duration: {assessmentData.sleep_duration} hours
          </label>
          <input
            type="range"
            id="sleep_duration"
            min="0"
            max="12"
            step="0.5"
            value={assessmentData.sleep_duration}
            onChange={(e) => updateAssessmentValue('sleep_duration', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>0</span>
            <span>7-9 (Optimal)</span>
            <span>12</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="sleep_quality">
            Sleep Quality: {assessmentData.sleep_quality}/5
          </label>
          <input
            type="range"
            id="sleep_quality"
            min="1"
            max="5"
            value={assessmentData.sleep_quality}
            onChange={(e) => updateAssessmentValue('sleep_quality', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>1 (Poor)</span>
            <span>3 (Average)</span>
            <span>5 (Excellent)</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="emotional_exhaustion">
            Emotional Exhaustion Level: {assessmentData.emotional_exhaustion}/5
          </label>
          <input
            type="range"
            id="emotional_exhaustion"
            min="1"
            max="5"
            value={assessmentData.emotional_exhaustion}
            onChange={(e) => updateAssessmentValue('emotional_exhaustion', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>1 (Low)</span>
            <span>3 (Moderate)</span>
            <span>5 (High)</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="motivation_level">
            Motivation and Engagement: {assessmentData.motivation_level}/5
          </label>
          <input
            type="range"
            id="motivation_level"
            min="1"
            max="5"
            value={assessmentData.motivation_level}
            onChange={(e) => updateAssessmentValue('motivation_level', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>1 (Low)</span>
            <span>3 (Moderate)</span>
            <span>5 (High)</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="screen_time">
            Screen Time per Day: {assessmentData.screen_time} hours
          </label>
          <input
            type="range"
            id="screen_time"
            min="0"
            max="16"
            step="0.5"
            value={assessmentData.screen_time}
            onChange={(e) => updateAssessmentValue('screen_time', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>0</span>
            <span>8 (Average)</span>
            <span>16</span>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="perceived_stress">
            Perceived Stress Level: {assessmentData.perceived_stress}/5
          </label>
          <input
            type="range"
            id="perceived_stress"
            min="1"
            max="5"
            value={assessmentData.perceived_stress}
            onChange={(e) => updateAssessmentValue('perceived_stress', e.target.value)}
            className="range-input"
            required
          />
          <div className="range-labels">
            <span>1 (Low)</span>
            <span>3 (Moderate)</span>
            <span>5 (High)</span>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Processing...' : 'Submit Assessment'}
        </button>
      </form>
    </div>
  );
};

export default AssessmentForm;
