import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // URL of the FastAPI backend
  headers: {
    'Content-Type': 'application/json'
  }
});

// Optional: Add a request interceptor to include the token
import { useAuthStore } from '../stores/auth';

apiClient.interceptors.request.use(config => {
  const authStore = useAuthStore();
  const token = authStore.token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default apiClient;
