import React from 'react';
import { SubstitutionOption } from '../../../types/chord';
import MusicNotation from '../../common/MusicNotation';
import './ChordSubstitutionDisplay.css';

interface ChordSubstitutionDisplayProps {
  originalChord: string;
  substitutions: SubstitutionOption[];
  onSelectSubstitution?: (chord: string) => void;
}

const ChordSubstitutionDisplay: React.FC<ChordSubstitutionDisplayProps> = ({
  originalChord,
  substitutions,
  onSelectSubstitution,
}) => {
  const getTechniqueColor = (technique: string): string => {
    const colors: Record<string, string> = {
      tritone: '#ff6b6b',
      diatonic: '#4ecdc4',
      chromatic: '#95e1d3',
      'circle-of-fifths': '#f9ca24',
      random: '#a29bfe',
    };
    return colors[technique.toLowerCase()] || '#6c5ce7';
  };

  const getTechniqueLabel = (technique: string): string => {
    const labels: Record<string, string> = {
      tritone: 'Tritone Sub',
      diatonic: 'Diatonic',
      chromatic: 'Chromatic',
      'circle-of-fifths': 'Circle of 5ths',
      random: 'Random',
    };
    return labels[technique.toLowerCase()] || technique;
  };

  return (
    <div className="chord-substitution-display">
      <div className="original-chord-section">
        <h3>Original Chord</h3>
        <div className="chord-card original">
          <div className="chord-symbol-large">{originalChord}</div>
          <MusicNotation chords={[originalChord]} width={300} height={150} />
        </div>
      </div>

      <div className="substitutions-section">
        <h3>
          Suggested Substitutions
          <span className="substitution-count">({substitutions.length} options)</span>
        </h3>

        {substitutions.length === 0 ? (
          <div className="no-substitutions">
            <p>No substitutions available for this chord.</p>
          </div>
        ) : (
          <div className="substitutions-grid">
            {substitutions.map((sub, index) => (
              <div
                key={index}
                className="substitution-card"
                onClick={() => onSelectSubstitution?.(sub.chord)}
                role="button"
                tabIndex={0}
              >
                <div className="substitution-header">
                  <div className="chord-symbol">{sub.chord}</div>
                  <div
                    className="technique-badge"
                    style={{ background: getTechniqueColor(sub.technique) }}
                  >
                    {getTechniqueLabel(sub.technique)}
                  </div>
                </div>

                <div className="substitution-notation">
                  <MusicNotation chords={[sub.chord]} width={250} height={120} />
                </div>

                <div className="substitution-info">
                  <div className="description">{sub.description}</div>
                  {(sub.common_usage || sub.commonUsage) && (
                    <div className="common-usage">
                      <strong>Usage:</strong> {sub.common_usage || sub.commonUsage}
                    </div>
                  )}
                  <div className="score-bar">
                    <div className="score-label">Match Score</div>
                    <div className="score-track">
                      <div
                        className="score-fill"
                        style={{ width: `${sub.score * 100}%` }}
                      />
                    </div>
                    <div className="score-value">{(sub.score * 100).toFixed(0)}%</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChordSubstitutionDisplay;
