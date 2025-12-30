import apiClient from './api';
import type { UserCreate, UserRead, Token } from './types';

class AuthService {
  async login(username: string, password: string): Promise<Token> {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    try {
      const response = await apiClient.post<Token>('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    } catch (error) {
      console.error("Error during login:", error);
      throw error;
    }
  }

  async register(userData: UserCreate): Promise<UserRead> {
    try {
      const response = await apiClient.post<UserRead>('/auth/register', userData);
      return response.data;
    } catch (error) {
      console.error("Error during registration:", error);
      throw error;
    }
  }
}

export default new AuthService();
