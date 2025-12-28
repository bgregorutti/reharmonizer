export interface Chord {
  symbol: string;
  rootNote: string;
  notes: string[];
  intervals: number[];
  chordQuality?: string;
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
  commonUsage?: string;
  score: number;
}

export interface SubstitutionResponse {
  originalChord: string;
  substitutions: SubstitutionOption[];
}
