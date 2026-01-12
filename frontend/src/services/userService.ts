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

  /**
   * Like-olt einen Benutzer.
   * Erfordert Authentifizierung via Bearer Token.
   */
  async likeUser(userId: number): Promise<void> {
    try {
      await apiClient.post(`/users/like/${userId}`);
    } catch (error) {
      console.error("Error during like:", error);
      throw error;
    }
  }

  /**
   * Ruft eine Liste von Benutzern ab, die den aktuellen Benutzer geliked haben.
   * Erfordert Authentifizierung via Bearer Token.
   */
  async getUsersWhoLikedMe(): Promise<UserRead[]> {
    try {
      const response = await apiClient.get<UserRead[]>('/users/likes');
      return response.data;
    } catch (error) {
      console.error("Error during get likes:", error);
      throw error;
    }
  }

  /**
   * Ruft eine Liste von Benutzern ab, die der aktuelle Benutzer geliked hat.
   * Erfordert Authentifizierung via Bearer Token.
   */
  async getMyLikes(): Promise<UserRead[]> {
    try {
      const response = await apiClient.get<UserRead[]>('/users/my-likes');
      return response.data;
    } catch (error) {
      console.error("Error during get my likes:", error);
      throw error;
    }
  }
}

export default new UserService();

