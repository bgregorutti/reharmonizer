import React from 'react';
import type { MusicStyle, StyleOption } from '../../../types/melody';
import './StyleSelector.css';

interface StyleSelectorProps {
  selectedStyle: MusicStyle;
  onStyleChange: (style: MusicStyle) => void;
  onHarmonize: () => void;
  isLoading?: boolean;
}

const STYLE_OPTIONS: StyleOption[] = [
  {
    value: 'jazz',
    label: 'Jazz',
    description: 'Extended chords (7ths, 9ths), ii-V-I progressions, sophisticated harmony',
  },
  {
    value: 'pop',
    label: 'Pop',
    description: 'Simple triads, common progressions (I-V-vi-IV), accessible and catchy',
  },
  {
    value: 'classical',
    label: 'Classical',
    description: 'Functional harmony (I-IV-V), diatonic chords, strong voice leading',
  },
];

const StyleSelector: React.FC<StyleSelectorProps> = ({
  selectedStyle,
  onStyleChange,
  onHarmonize,
  isLoading = false,
}) => {
  return (
    <div className="style-selector">
      <h3>Choose Harmonization Style</h3>

      <div className="style-options">
        {STYLE_OPTIONS.map((option) => (
          <div
            key={option.value}
            className={`style-option ${selectedStyle === option.value ? 'selected' : ''} ${isLoading ? 'disabled' : ''}`}
            onClick={() => !isLoading && onStyleChange(option.value)}
          >
            <div className="style-header">
              <div className="style-radio">
                {selectedStyle === option.value && <div className="radio-dot"></div>}
              </div>
              <h4>{option.label}</h4>
            </div>
            <p className="style-description">{option.description}</p>
          </div>
        ))}
      </div>

      <button
        className="harmonize-button"
        onClick={onHarmonize}
        disabled={isLoading}
      >
        {isLoading ? (
          <>
            <span className="button-spinner"></span>
            Harmonizing...
          </>
        ) : (
          <>
            Generate Harmonization
          </>
        )}
      </button>
    </div>
  );
};

export default StyleSelector;
