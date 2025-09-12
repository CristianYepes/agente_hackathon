// frontend/src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log('🔗 API Base URL:', API_BASE_URL);

class ApiService {
  async makeRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    console.log(`🔄 ${config.method || 'GET'} ${url}`);

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Response received');
      return data;
    } catch (error) {
      console.error('❌ API Error:', error.message);
      throw error;
    }
  }

  async sendMessage(message, sessionId = null, location = null, familyProfile = null) {
    return this.makeRequest('/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        session_id: sessionId,
        location,
        family_profile: familyProfile
      })
    });
  }

  async getLocations() {
    return this.makeRequest('/madrid-locations');
  }

  async healthCheck() {
    return this.makeRequest('/health');
  }
}

// Exportar instancia con nombre para evitar warning de ESLint
const apiService = new ApiService();
export default apiService;
