import { apiService, API_ENDPOINTS } from './api';
import API_CONFIG from '../config/api';

/**
 * Authentication Service
 * Handles user authentication, authorization, and session management
 */
export const authService = {
  // Login user
  login: async (credentials) => {
    try {
      const response = await apiService.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
      
      // Store token if authentication is enabled
      if (API_CONFIG.AUTH.ENABLED && response.token) {
        localStorage.setItem(API_CONFIG.AUTH.TOKEN_KEY, response.token);
      }
      
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      // Call logout endpoint if authentication is enabled
      if (API_CONFIG.AUTH.ENABLED) {
        await apiService.post(API_ENDPOINTS.AUTH.LOGOUT);
      }
      
      // Clear local storage
      localStorage.removeItem(API_CONFIG.AUTH.TOKEN_KEY);
      
      return { success: true };
    } catch (error) {
      console.error('Logout error:', error);
      // Still clear local storage even if API call fails
      localStorage.removeItem(API_CONFIG.AUTH.TOKEN_KEY);
      throw error;
    }
  },

  // Register new user
  register: async (userData) => {
    try {
      const response = await apiService.post(API_ENDPOINTS.AUTH.REGISTER, userData);
      return response;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Get current user profile
  getProfile: async () => {
    try {
      return await apiService.get(API_ENDPOINTS.AUTH.PROFILE);
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  },

  // Update user profile
  updateProfile: async (profileData) => {
    try {
      return await apiService.put(API_ENDPOINTS.AUTH.PROFILE, profileData);
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  },

  // Change password
  changePassword: async (passwordData) => {
    try {
      return await apiService.post(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, passwordData);
    } catch (error) {
      console.error('Change password error:', error);
      throw error;
    }
  },

  // Refresh token
  refreshToken: async () => {
    try {
      const response = await apiService.post(API_ENDPOINTS.AUTH.REFRESH);
      
      // Update stored token
      if (API_CONFIG.AUTH.ENABLED && response.token) {
        localStorage.setItem(API_CONFIG.AUTH.TOKEN_KEY, response.token);
      }
      
      return response;
    } catch (error) {
      console.error('Token refresh error:', error);
      throw error;
    }
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    if (!API_CONFIG.AUTH.ENABLED) {
      return true; // If auth is disabled, consider user authenticated
    }
    
    const token = localStorage.getItem(API_CONFIG.AUTH.TOKEN_KEY);
    return !!token;
  },

  // Get stored token
  getToken: () => {
    if (!API_CONFIG.AUTH.ENABLED) {
      return null;
    }
    
    return localStorage.getItem(API_CONFIG.AUTH.TOKEN_KEY);
  },

  // Clear authentication data
  clearAuth: () => {
    localStorage.removeItem(API_CONFIG.AUTH.TOKEN_KEY);
  },

  // Check token expiry and refresh if needed
  checkTokenExpiry: async () => {
    if (!API_CONFIG.AUTH.ENABLED) {
      return true;
    }

    const token = localStorage.getItem(API_CONFIG.AUTH.TOKEN_KEY);
    if (!token) {
      return false;
    }

    try {
      // Decode token to check expiry (basic implementation)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Math.floor(Date.now() / 1000);
      const timeUntilExpiry = payload.exp - now;

      // If token expires within the refresh threshold, refresh it
      if (timeUntilExpiry < API_CONFIG.AUTH.REFRESH_THRESHOLD) {
        await authService.refreshToken();
      }

      return true;
    } catch (error) {
      console.error('Token validation error:', error);
      authService.clearAuth();
      return false;
    }
  },
};

export default authService;
