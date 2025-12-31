import React, { useState } from 'react';
import type {
  HarmonizationResponse,
  MelodyNote,
} from '../../../types/melody';
import TwoStaveScore from '../../common/TwoStaveScore';
import './HarmonizationResults.css';

interface HarmonizationResultsProps {
  result: HarmonizationResponse;
  melodyNotes: MelodyNote[];
  timeSignature?: string;
  keySignature?: string;
}

const HarmonizationResults: React.FC<HarmonizationResultsProps> = ({
  result,
  melodyNotes,
  timeSignature = '4/4',
  keySignature = 'C',
}) => {
  const [selectedAlternative, setSelectedAlternative] = useState<number | null>(null);

  // Determine which chord timing to display
  const displayChordTiming =
    selectedAlternative !== null && result.alternatives_timing
      ? result.alternatives_timing[selectedAlternative]
      : result.chord_timing;

  const displayTitle =
    selectedAlternative !== null
      ? `Alternative ${selectedAlternative + 1}`
      : 'Primary Harmonization';

  const handleDownload = async (format: 'musicxml' | 'pdf') => {
    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/melody/harmonization/${result.id}/export/${format}`
      );

      if (!response.ok) {
        const error = await response.json();
        alert(`Download failed: ${error.detail || 'Unknown error'}`);
        return;
      }

      // Create blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `harmonization_${result.id}.${format === 'musicxml' ? 'musicxml' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download file. Please try again.');
    }
  };

  return (
    <div className="harmonization-results">
      <div className="results-header">
        <h3>Harmonization Results</h3>
        <div className="style-badge">{result.style.toUpperCase()}</div>
      </div>

      {result.pattern_applied && (
        <div className="pattern-info">
          <span className="pattern-label">Pattern:</span>
          <span className="pattern-name">{result.pattern_applied}</span>
          <span className="pattern-score">Score: {(result.score * 100).toFixed(0)}%</span>
        </div>
      )}

      {/* Tabbed alternatives selector */}
      {result.alternatives && result.alternatives.length > 0 && (
        <div className="alternatives-section">
          <h4>View Alternatives</h4>
          <div className="alternatives-tabs">
            <button
              className={`alt-tab ${selectedAlternative === null ? 'active' : ''}`}
              onClick={() => setSelectedAlternative(null)}
            >
              Primary
            </button>
            {result.alternatives.map((_, index) => (
              <button
                key={index}
                className={`alt-tab ${selectedAlternative === index ? 'active' : ''}`}
                onClick={() => setSelectedAlternative(index)}
              >
                Alt {index + 1}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Two-stave score - rerenders when alternative changes */}
      <div className="score-section">
        <h4>{displayTitle}</h4>
        <TwoStaveScore
          melodyNotes={melodyNotes}
          chordTiming={displayChordTiming}
          width={900}
          height={400}
          timeSignature={timeSignature}
          keySignature={keySignature}
        />
      </div>

      {/* Chord progression text summary */}
      <div className="progression-summary">
        <h4>Chord Progression</h4>
        <div className="chord-chips">
          {displayChordTiming.map((chord, idx) => (
            <span key={idx} className="chord-chip">
              {chord.symbol}
              <span className="chord-measure">m.{chord.measure}</span>
            </span>
          ))}
        </div>
      </div>

      <div className="results-footer">
        <div className="download-section">
          <h4>Download Results</h4>
          <div className="download-buttons">
            <button
              className="download-button"
              onClick={() => handleDownload('musicxml')}
            >
              📄 Download MusicXML
            </button>
            <button
              className="download-button"
              onClick={() => handleDownload('pdf')}
            >
              📑 Download PDF
            </button>
          </div>
        </div>
        <p className="results-tip">
          Click alternative tabs above to rerender the entire score with different harmonizations
        </p>
      </div>
    </div>
  );
};

export default HarmonizationResults;
