/**
 * API service for melody harmonization endpoints
 */

import api from './api';
import type {
  MelodyUploadResponse,
  HarmonizationRequest,
  HarmonizationResponse,
} from '../types/melody';

const BASE_URL = '/melody';

export const melodyService = {
  /**
   * Upload and analyze a melody file (MusicXML or MSCZ)
   */
  uploadMelody: async (file: File): Promise<MelodyUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<MelodyUploadResponse>(
      `${BASE_URL}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  /**
   * Generate harmonization for an uploaded melody
   */
  harmonize: async (
    request: HarmonizationRequest
  ): Promise<HarmonizationResponse> => {
    const response = await api.post<HarmonizationResponse>(
      `${BASE_URL}/harmonize`,
      request
    );

    return response.data;
  },

  /**
   * Get melody upload by ID
   */
  getMelodyUpload: async (uploadId: number): Promise<MelodyUploadResponse> => {
    const response = await api.get<MelodyUploadResponse>(
      `${BASE_URL}/uploads/${uploadId}`
    );

    return response.data;
  },
};
