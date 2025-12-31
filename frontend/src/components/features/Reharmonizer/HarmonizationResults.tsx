import React, { useState } from 'react';
import type { HarmonizationResponse } from '../../../types/melody';
import MusicNotation from '../../common/MusicNotation';
import './HarmonizationResults.css';

interface HarmonizationResultsProps {
  result: HarmonizationResponse;
}

const HarmonizationResults: React.FC<HarmonizationResultsProps> = ({ result }) => {
  const [selectedAlternative, setSelectedAlternative] = useState<number | null>(null);

  const displayProgression = selectedAlternative !== null && result.alternatives
    ? result.alternatives[selectedAlternative]
    : result.chord_progression;

  const displayTitle = selectedAlternative !== null
    ? `Alternative ${selectedAlternative + 1}`
    : 'Primary Harmonization';

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

      <div className="progression-section">
        <h4>{displayTitle}</h4>
        <div className="chord-progression">
          {displayProgression.map((chord, index) => (
            <div key={index} className="chord-item">
              <MusicNotation chord={chord} />
              <span className="chord-label">{chord}</span>
            </div>
          ))}
        </div>
      </div>

      {result.alternatives && result.alternatives.length > 0 && (
        <div className="alternatives-section">
          <h4>Alternative Harmonizations</h4>
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

          {selectedAlternative !== null && (
            <div className="alternative-preview">
              {result.alternatives[selectedAlternative].map((chord, idx) => (
                <span key={idx} className="chord-chip">{chord}</span>
              ))}
            </div>
          )}
        </div>
      )}

      <div className="results-footer">
        <p className="results-tip">
          💡 Try different styles to explore various harmonization approaches!
        </p>
      </div>
    </div>
  );
};

export default HarmonizationResults;
