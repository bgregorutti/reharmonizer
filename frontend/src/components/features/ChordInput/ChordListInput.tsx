import React, { useState, useEffect } from 'react';
import chordService from '../../../services/chordService';
import { Chord } from '../../../types/chord';
import './ChordListInput.css';

interface ChordListInputProps {
  onChordsChange: (chords: string[]) => void;
}

const ChordListInput: React.FC<ChordListInputProps> = ({ onChordsChange }) => {
  const [inputValue, setInputValue] = useState('');
  const [chordList, setChordList] = useState<string[]>([]);
  const [availableChords, setAvailableChords] = useState<Chord[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    // Load available chords from backend
    const loadChords = async () => {
      try {
        const chords = await chordService.getChords();
        setAvailableChords(chords);
      } catch (error) {
        console.error('Failed to load chords:', error);
      }
    };
    loadChords();
  }, []);

  useEffect(() => {
    // Update suggestions based on input
    if (inputValue.trim()) {
      const filtered = availableChords
        .filter((chord) =>
          chord.symbol.toLowerCase().startsWith(inputValue.toLowerCase())
        )
        .map((chord) => chord.symbol)
        .slice(0, 10);
      setSuggestions(filtered);
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [inputValue, availableChords]);

  const handleAddChord = (chord: string) => {
    if (chord.trim() && !chordList.includes(chord)) {
      const newChordList = [...chordList, chord.trim()];
      setChordList(newChordList);
      onChordsChange(newChordList);
      setInputValue('');
      setShowSuggestions(false);
    }
  };

  const handleRemoveChord = (index: number) => {
    const newChordList = chordList.filter((_, i) => i !== index);
    setChordList(newChordList);
    onChordsChange(newChordList);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && inputValue.trim()) {
      handleAddChord(inputValue);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleAddChord(suggestion);
  };

  const handleClear = () => {
    setChordList([]);
    onChordsChange([]);
    setInputValue('');
  };

  return (
    <div className="chord-list-input">
      <h3>Enter Chord Progression (Modern Music)</h3>

      <div className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type chord symbol (e.g., Cmaj7, Dm7, G7)..."
            className="chord-input"
          />
          <button
            onClick={() => handleAddChord(inputValue)}
            className="add-btn"
            disabled={!inputValue.trim()}
          >
            Add
          </button>
        </div>

        {showSuggestions && suggestions.length > 0 && (
          <div className="suggestions-dropdown">
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className="suggestion-item"
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </div>
            ))}
          </div>
        )}
      </div>

      {chordList.length > 0 && (
        <div className="chord-list-display">
          <div className="chord-list-header">
            <span className="chord-count">
              {chordList.length} chord{chordList.length !== 1 ? 's' : ''}
            </span>
            <button onClick={handleClear} className="clear-btn">
              Clear All
            </button>
          </div>

          <div className="chord-chips">
            {chordList.map((chord, index) => (
              <div key={index} className="chord-chip">
                <span className="chord-symbol">{chord}</span>
                <button
                  onClick={() => handleRemoveChord(index)}
                  className="remove-btn"
                  aria-label="Remove chord"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="help-text">
        <strong>Tip:</strong> Press Enter or click Add to add a chord. Common chord types:
        maj7, m7, 7, dim, aug, sus4, 6, 9, 13
      </div>
    </div>
  );
};

export default ChordListInput;
