import apiClient from './api';
import { ReharmonizationRequest, ReharmonizationResponse } from '../types/api';

export const reharmonizationService = {
  async reharmonize(request: ReharmonizationRequest): Promise<ReharmonizationResponse> {
    const response = await apiClient.post('/reharmonize', request);
    return response.data;
  },

  async getPatterns(genre?: string, complexity?: number) {
    const response = await apiClient.get('/patterns', {
      params: { genre, complexity },
    });
    return response.data;
  },
};

export default reharmonizationService;
