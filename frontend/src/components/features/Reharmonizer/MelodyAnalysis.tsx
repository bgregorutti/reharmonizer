import React from 'react';
import type { MelodyAnalysis as MelodyAnalysisType } from '../../../types/melody';
import './MelodyAnalysis.css';

interface MelodyAnalysisProps {
  analysis: MelodyAnalysisType;
  fileName: string;
}

const MelodyAnalysis: React.FC<MelodyAnalysisProps> = ({ analysis, fileName }) => {
  return (
    <div className="melody-analysis">
      <h3>Analysis Results</h3>

      <div className="analysis-card">
        <div className="file-info">
          <span className="label">File:</span>
          <span className="value">{fileName}</span>
        </div>

        <div className="analysis-grid">
          <div className="analysis-item">
            <span className="label">Detected Key</span>
            <span className="value key">{analysis.detected_key || 'Unknown'}</span>
          </div>

          <div className="analysis-item">
            <span className="label">Time Signature</span>
            <span className="value">{analysis.time_signature || 'N/A'}</span>
          </div>

          <div className="analysis-item">
            <span className="label">Tempo</span>
            <span className="value">{analysis.tempo ? `${analysis.tempo} BPM` : 'N/A'}</span>
          </div>

          <div className="analysis-item">
            <span className="label">Measures</span>
            <span className="value">{analysis.measures}</span>
          </div>

          <div className="analysis-item">
            <span className="label">Notes</span>
            <span className="value">{analysis.notes.filter(n => !n.is_rest).length}</span>
          </div>

          <div className="analysis-item">
            <span className="label">Duration</span>
            <span className="value">{analysis.duration.toFixed(1)} beats</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MelodyAnalysis;
