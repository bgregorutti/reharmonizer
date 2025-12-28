export interface KeySignature {
  keyName: string;
  tonic: string;
  mode: 'major' | 'minor';
  sharpsFlats: number;
  accidentals: string[];
  scaleNotes: string[];
}

export interface KeySignatureWithChords extends KeySignature {
  diatonicChords: string[];
}
