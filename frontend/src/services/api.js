/**
 * API service for communicating with the backend.
 */
import axios from 'axios';

// const API_BASE_URL =
//   process.env.REACT_APP_API_URL ||
//   'https://ibm-skill-build-project-production.up.railway.app/api';

const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  'https://ibm-skill-build-project-production.up.railway.app/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// User endpoints
export const createUser = async (userData) => {
  try {
    const response = await api.post('/users/', userData);
    return response.data;
  } catch (error) {
    // Log detailed error for debugging
    if (error.response) {
      // Server responded with error status
      console.error('API Error Response:', error.response.status, error.response.data);
      throw error;
    } else if (error.request) {
      // Request made but no response received
      console.error('No response from server:', error.request);
      throw new Error('Cannot connect to backend server. Check API_BASE_URL and deployment status.');
    } else {
      // Error setting up request
      console.error('Request setup error:', error.message);
      throw error;
    }
  }
};

export const getUser = async (userId) => {
  const response = await api.get(`/users/${userId}`);
  return response.data;
};

// Assessment endpoints
export const createAssessment = async (assessmentData) => {
  const response = await api.post('/assessments/', assessmentData);
  return response.data;
};

export const getAssessment = async (assessmentId) => {
  const response = await api.get(`/assessments/${assessmentId}`);
  return response.data;
};

export const getAssessmentDetails = async (assessmentId) => {
  const response = await api.get(`/assessments/${assessmentId}/details`);
  return response.data;
};

export const getUserAssessments = async (userId) => {
  const response = await api.get(`/assessments/user/${userId}`);
  return response.data;
};

// Recovery plan endpoints
export const generateRecoveryPlan = async (planData) => {
  const response = await api.post('/recovery/generate', planData);
  return response.data;
};

export const getLatestRecoveryPlan = async (userId) => {
  const response = await api.get(`/recovery/user/${userId}/latest`);
  return response.data;
};

export const getRecoveryPlan = async (planId) => {
  const response = await api.get(`/recovery/${planId}`);
  return response.data;
};

// Progress endpoints
export const createProgressRecord = async (progressData) => {
  const response = await api.post('/progress/', progressData);
  return response.data;
};

export const getUserProgress = async (userId) => {
  const response = await api.get(`/progress/user/${userId}`);
  return response.data;
};

export const getProgressAnalysis = async (userId) => {
  const response = await api.get(`/progress/user/${userId}/analysis`);
  return response.data;
};

export default api;
