/**
 * AI Mentor Service
 * Handles API calls to the AI mentor backend
 */
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Send a chat message to AI mentor
 */
export const sendChatMessage = async (message, conversationId = null) => {
  try {
    const response = await apiClient.post('/ai/chat', {
      message,
      conversation_id: conversationId,
    });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Generate a study plan
 */
export const generateStudyPlan = async (durationDays, subjects, focusAreas = null) => {
  try {
    const response = await apiClient.post('/ai/study-plan', {
      duration_days: durationDays,
      subjects,
      focus_areas: focusAreas,
    });
    return response.data;
  } catch (error) {
    console.error('Error generating study plan:', error);
    throw error;
  }
};

/**
 * Get personalized recommendations
 */
export const getRecommendations = async (includePerformance = false) => {
  try {
    const response = await apiClient.post('/ai/recommendations', {
      include_performance: includePerformance,
    });
    return response.data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

/**
 * Get chat history
 */
export const getChatHistory = async (limit = 50) => {
  try {
    const response = await apiClient.get('/ai/history', {
      params: { limit },
    });
    return response.data;
  } catch (error) {
    console.error('Error getting chat history:', error);
    throw error;
  }
};

/**
 * Check AI service status
 */
export const getAIStatus = async () => {
  try {
    const response = await apiClient.get('/ai/status');
    return response.data;
  } catch (error) {
    console.error('Error checking AI status:', error);
    throw error;
  }
};

export default {
  sendChatMessage,
  generateStudyPlan,
  getRecommendations,
  getChatHistory,
  getAIStatus,
};
