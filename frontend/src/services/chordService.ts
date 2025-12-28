import apiClient from './api';
import { Chord, SubstitutionRequest, SubstitutionResponse } from '../types/chord';

export const chordService = {
  async getChords(): Promise<Chord[]> {
    const response = await apiClient.get('/chords');
    return response.data;
  },

  async getChord(symbol: string): Promise<Chord> {
    const response = await apiClient.get(`/chords/${symbol}`);
    return response.data;
  },

  async getChordNotes(symbol: string) {
    const response = await apiClient.get(`/chords/${symbol}/notes`);
    return response.data;
  },

  async getChordExtensions(symbol: string) {
    const response = await apiClient.get(`/chords/${symbol}/extensions`);
    return response.data;
  },

  async getSubstitutions(request: SubstitutionRequest): Promise<SubstitutionResponse> {
    const response = await apiClient.post('/reharmonize/substitutions/analyze', request);
    return response.data;
  },
};

export default chordService;
