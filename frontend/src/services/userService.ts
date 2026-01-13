import apiClient from './api';
import type { UserRead } from './types';

class UserService {
  /**
   * Fetches a compatible user from the backend.
   * Requires authentication via Bearer token.
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
   * Records a swipe action (like or dislike) for a user.
   * Requires authentication via Bearer token.
   * @param userId The ID of the user being swiped on.
   * @param isLike A boolean indicating if it's a like (true) or dislike (false).
   */
  async swipeUser(userId: number, isLike: boolean): Promise<{ message: string; match_id?: number }> {
    try {
      const response = await apiClient.post(`/users/swipe/${userId}/${isLike}`);
      return response.data;
    } catch (error) {
      console.error("Error during swipe:", error);
      throw error;
    }
  }

  /**
   * Fetches a list of users who liked the current user.
   * Requires authentication via Bearer token.
   */
  async getUsersWhoLikedMe(): Promise<UserRead[]> {
    try {
      const response = await apiClient.get<UserRead[]>('/users/likes');
      return response.data;
    } catch (error) {
      console.error("Error fetching users who liked me:", error);
      throw error;
    }
  }

  /**
   * Fetches a list of users the current user has liked.
   * Requires authentication via Bearer token.
   */
  async getMyLikes(): Promise<UserRead[]> {
    try {
      const response = await apiClient.get<UserRead[]>('/users/my-likes');
      return response.data;
    } catch (error) {
      console.error("Error fetching my likes:", error);
      throw error;
    }
  }
}

export default new UserService();