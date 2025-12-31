/**
 * TypeScript types for melody harmonization feature
 */

export interface MelodyNote {
  type: string;
  pitch: string | null;
  pitch_class: string | null;
  midi: number | null;
  duration: number;
  offset: number;
  measure: number | null;
  is_rest: boolean;
  chord_notes?: string[];
}

export interface MelodyAnalysis {
  notes: MelodyNote[];
  detected_key: string | null;
  time_signature: string | null;
  tempo: number | null;
  measures: number;
  duration: number;
  parts: number;
}

export interface MelodyUploadResponse {
  id: number;
  file_name: string;
  file_type: string;
  analysis: MelodyAnalysis;
}

export interface ChordRecommendation {
  symbol: string;
  root_note: string;
  notes: string[];
  chord_quality: string;
  score: number;
}

export interface ChordTiming {
  symbol: string;
  measure: number;
  offset: number;
  duration: number;
}

export interface HarmonizationRequest {
  melody_upload_id: number;
  style: string;
  options?: Record<string, any>;
}

export interface HarmonizationResponse {
  id: number;
  melody_upload_id: number;
  style: string;
  chord_progression: string[];
  chord_details: ChordRecommendation[];
  chord_timing: ChordTiming[];
  pattern_applied: string | null;
  score: number;
  alternatives: string[][] | null;
  alternatives_timing: ChordTiming[][] | null;
}

export type MusicStyle = 'jazz' | 'pop' | 'classical';

export interface StyleOption {
  value: MusicStyle;
  label: string;
  description: string;
}
