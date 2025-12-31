import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { melodyService } from '../../../services/melodyService';
import type {
  MelodyUploadResponse,
  HarmonizationResponse,
  MusicStyle,
} from '../../../types/melody';
import MelodyUpload from './MelodyUpload';
import MelodyAnalysis from './MelodyAnalysis';
import StyleSelector from './StyleSelector';
import HarmonizationResults from './HarmonizationResults';
import './ReharmonizerView.css';

const ReharmonizerView: React.FC = () => {
  const navigate = useNavigate();
  const [uploadedMelody, setUploadedMelody] = useState<MelodyUploadResponse | null>(null);
  const [selectedStyle, setSelectedStyle] = useState<MusicStyle>('jazz');
  const [harmonization, setHarmonization] = useState<HarmonizationResponse | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isHarmonizing, setIsHarmonizing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    setHarmonization(null);

    try {
      const result = await melodyService.uploadMelody(file);
      setUploadedMelody(result);
    } catch (err) {
      setError('Failed to upload and analyze melody. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleHarmonize = async () => {
    if (!uploadedMelody) return;

    setIsHarmonizing(true);
    setError(null);

    try {
      const result = await melodyService.harmonize({
        melody_upload_id: uploadedMelody.id,
        style: selectedStyle,
      });
      setHarmonization(result);
    } catch (err) {
      setError('Failed to generate harmonization. Please try again.');
      console.error('Harmonization error:', err);
    } finally {
      setIsHarmonizing(false);
    }
  };

  const handleStyleChange = (style: MusicStyle) => {
    setSelectedStyle(style);
    // Clear previous harmonization when style changes
    setHarmonization(null);
  };

  return (
    <div className="reharmonizer-view">
      <button
        className="nav-button nav-back"
        onClick={() => navigate('/substitution')}
        title="Go to Chord Substitutions"
      >
        ← Chord Substitutions
      </button>

      <div className="view-header">
        <h1>Reharmonizer</h1>
        <p className="view-subtitle">
          Upload a melody and generate chord progressions in different styles
        </p>
      </div>

      <div className="view-content">
        {/* Step 1: Upload */}
        <MelodyUpload onUpload={handleFileUpload} isLoading={isUploading} />

        {/* Error message */}
        {error && (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {/* Step 2: Analysis */}
        {uploadedMelody && (
          <MelodyAnalysis
            analysis={uploadedMelody.analysis}
            fileName={uploadedMelody.file_name}
          />
        )}

        {/* Step 3: Style Selection */}
        {uploadedMelody && (
          <StyleSelector
            selectedStyle={selectedStyle}
            onStyleChange={handleStyleChange}
            onHarmonize={handleHarmonize}
            isLoading={isHarmonizing}
          />
        )}

        {/* Step 4: Results */}
        {harmonization && uploadedMelody && (
          <HarmonizationResults
            result={harmonization}
            melodyNotes={uploadedMelody.analysis.notes}
            timeSignature={uploadedMelody.analysis.time_signature || '4/4'}
            keySignature={uploadedMelody.analysis.detected_key || 'C'}
          />
        )}
      </div>
    </div>
  );
};

export default ReharmonizerView;
