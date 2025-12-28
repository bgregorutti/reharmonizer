export interface Chord {
  id?: number;
  symbol: string;
  root_note: string;
  rootNote?: string; // Alias for compatibility
  notes: string[];
  intervals: string[];
  chord_quality?: string;
  chordQuality?: string; // Alias for compatibility
}

export interface ChordWithExtensions extends Chord {
  extensions: string[];
  tensions: string[];
  avoidNotes?: string[];
}

export interface SubstitutionContext {
  key?: string;
  previousChord?: string;
  nextChord?: string;
  position?: string;
}

export interface SubstitutionRequest {
  chord: string;
  context?: SubstitutionContext;
  techniques?: string[];
}

export interface SubstitutionOption {
  chord: string;
  technique: string;
  description: string;
  common_usage?: string;
  commonUsage?: string; // Alias for compatibility
  score: number;
}

export interface SubstitutionResponse {
  original_chord: string;
  originalChord?: string; // Alias for compatibility
  substitutions: SubstitutionOption[];
}

export interface ImprovisationNotesResponse {
  chord_symbol: string;
  chord_tones: string[];
  scale_notes: string[];
  recommended_notes: string[];
  avoid_notes: string[];
}
