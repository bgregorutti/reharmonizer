export interface ReharmonizationRequest {
  keySignature?: string;
  chords: string[];
  options?: {
    techniques?: string[];
    complexity?: number;
    genre?: string;
  };
}

export interface ReharmonizationSuggestion {
  chords: string[];
  technique: string;
  score: number;
  analysis: Record<string, any>;
}

export interface ReharmonizationResponse {
  original: string[];
  suggestions: ReharmonizationSuggestion[];
  analysis: Record<string, any>;
}
