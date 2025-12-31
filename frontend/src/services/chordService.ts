import apiClient from './api';
import {
  Chord,
  SubstitutionRequest,
  SubstitutionResponse,
  ImprovisationNotesResponse
} from '../types/chord';

export const chordService = {
  async getChords(): Promise<Chord[]> {
    const response = await apiClient.get('/chords/');
    return response.data;
  },

  async getChordsByKey(keySignature: string): Promise<Chord[]> {
    const response = await apiClient.get(`/keys/${keySignature}/chords`);
    // Backend returns {key: string, chords: Chord[], message: string}
    return response.data.chords || [];
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

  async getSubstitutions(
    chordSymbol: string,
    technique: string = 'random'
  ): Promise<SubstitutionResponse> {
    const response = await apiClient.get(`/reharmonize/substitutions/${chordSymbol}`, {
      params: { technique },
    });
    return response.data;
  },

  async getSubstitutionsWithContext(request: SubstitutionRequest): Promise<SubstitutionResponse> {
    const response = await apiClient.post('/reharmonize/substitutions/analyze', request);
    return response.data;
  },

  async getImprovisationNotes(
    chordSymbol: string,
    count: number = 5
  ): Promise<ImprovisationNotesResponse> {
    const response = await apiClient.get(`/improvisation/notes/${chordSymbol}`, {
      params: { count },
    });
    return response.data;
  },

  async searchChordsByNote(
    note: string,
    scaleType: string = 'major'
  ): Promise<Chord[]> {
    const response = await apiClient.get('/chords/search/by-note', {
      params: { note, scale_type: scaleType },
    });
    return response.data;
  },
};

export default chordService;
