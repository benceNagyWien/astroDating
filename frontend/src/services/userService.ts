import apiClient from './api';
import type { UserRead } from './types';

class UserService {
  /**
   * Ruft einen kompatiblen Benutzer vom Backend ab.
   * Erfordert Authentifizierung via Bearer Token.
   */
  async discoverCompatibleUser(): Promise<UserRead> {
    try {
      const response = await apiClient.get<UserRead>('/users/discover');
      return response.data;
    } catch (error) {
      console.error("Error during discover:", error);
      throw error;
    }
  }
}

export default new UserService();

