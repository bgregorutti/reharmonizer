import React, { useState } from 'react';
import './KeySignatureInput.css';

interface KeySignatureInputProps {
  onKeySignatureSelect: (keySignature: string) => void;
}

const KeySignatureInput: React.FC<KeySignatureInputProps> = ({ onKeySignatureSelect }) => {
  const [selectedKey, setSelectedKey] = useState<string>('');
  const [selectedQuality, setSelectedQuality] = useState<'major' | 'minor'>('major');

  // All possible key signatures
  const majorKeys = [
    'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#',
    'F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb'
  ];

  const minorKeys = [
    'Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'A#m',
    'Dm', 'Gm', 'Cm', 'Fm', 'Bbm', 'Ebm', 'Abm'
  ];

  // Number of sharps/flats for each key
  const keySignatures: Record<string, { type: 'sharp' | 'flat'; count: number }> = {
    'C': { type: 'sharp', count: 0 },
    'G': { type: 'sharp', count: 1 },
    'D': { type: 'sharp', count: 2 },
    'A': { type: 'sharp', count: 3 },
    'E': { type: 'sharp', count: 4 },
    'B': { type: 'sharp', count: 5 },
    'F#': { type: 'sharp', count: 6 },
    'C#': { type: 'sharp', count: 7 },
    'F': { type: 'flat', count: 1 },
    'Bb': { type: 'flat', count: 2 },
    'Eb': { type: 'flat', count: 3 },
    'Ab': { type: 'flat', count: 4 },
    'Db': { type: 'flat', count: 5 },
    'Gb': { type: 'flat', count: 6 },
    'Cb': { type: 'flat', count: 7 },
    // Minor keys
    'Am': { type: 'sharp', count: 0 },
    'Em': { type: 'sharp', count: 1 },
    'Bm': { type: 'sharp', count: 2 },
    'F#m': { type: 'sharp', count: 3 },
    'C#m': { type: 'sharp', count: 4 },
    'G#m': { type: 'sharp', count: 5 },
    'D#m': { type: 'sharp', count: 6 },
    'A#m': { type: 'sharp', count: 7 },
    'Dm': { type: 'flat', count: 1 },
    'Gm': { type: 'flat', count: 2 },
    'Cm': { type: 'flat', count: 3 },
    'Fm': { type: 'flat', count: 4 },
    'Bbm': { type: 'flat', count: 5 },
    'Ebm': { type: 'flat', count: 6 },
    'Abm': { type: 'flat', count: 7 },
  };

  const handleKeySelect = (key: string) => {
    setSelectedKey(key);
    onKeySignatureSelect(key);
  };

  const handleQualityChange = (quality: 'major' | 'minor') => {
    setSelectedQuality(quality);
    setSelectedKey('');
  };

  const displayKeys = selectedQuality === 'major' ? majorKeys : minorKeys;

  return (
    <div className="key-signature-input">
      <h3>Select Key Signature (Classical Music)</h3>

      <div className="quality-selector">
        <button
          className={`quality-btn ${selectedQuality === 'major' ? 'active' : ''}`}
          onClick={() => handleQualityChange('major')}
        >
          Major
        </button>
        <button
          className={`quality-btn ${selectedQuality === 'minor' ? 'active' : ''}`}
          onClick={() => handleQualityChange('minor')}
        >
          Minor
        </button>
      </div>

      <div className="key-grid">
        {displayKeys.map((key) => {
          const sig = keySignatures[key];
          const isSelected = selectedKey === key;

          return (
            <button
              key={key}
              className={`key-button ${isSelected ? 'selected' : ''}`}
              onClick={() => handleKeySelect(key)}
            >
              <div className="key-name">{key}</div>
              <div className="key-signature-info">
                {sig.count === 0 ? (
                  'No sharps/flats'
                ) : (
                  <>
                    {sig.count} {sig.type === 'sharp' ? '♯' : '♭'}
                    {sig.count > 1 ? 's' : ''}
                  </>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {selectedKey && (
        <div className="selected-key-display">
          <strong>Selected Key:</strong> {selectedKey}
          {keySignatures[selectedKey] && (
            <span className="signature-details">
              {' '}({keySignatures[selectedKey].count === 0
                ? 'No accidentals'
                : `${keySignatures[selectedKey].count} ${
                    keySignatures[selectedKey].type === 'sharp' ? 'sharp' : 'flat'
                  }${keySignatures[selectedKey].count > 1 ? 's' : ''}`})
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default KeySignatureInput;
