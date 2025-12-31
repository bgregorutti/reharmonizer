import React, { useState } from 'react';
import './NoteSearchInput.css';

interface NoteSearchInputProps {
  onSearch: (note: string, scaleType: string) => void;
}

const NoteSearchInput: React.FC<NoteSearchInputProps> = ({ onSearch }) => {
  const [selectedNote, setSelectedNote] = useState<string>('C');
  const [selectedScaleType, setSelectedScaleType] = useState<string>('major');

  const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const scaleTypes = [
    { value: 'major', label: 'Major' },
    { value: 'minor', label: 'Minor' },
  ];

  const handleSearch = () => {
    onSearch(selectedNote, selectedScaleType);
  };

  return (
    <div className="note-search-input">
      <div className="search-header">
        <h2>🔍 Search Chords by Note</h2>
        <p className="search-description">
          Find all chords that contain a specific note in a given scale context
        </p>
      </div>

      <div className="search-controls">
        <div className="control-group">
          <label htmlFor="note-select">Select Note:</label>
          <div className="note-selector">
            {notes.map((note) => (
              <button
                key={note}
                className={`note-btn ${selectedNote === note ? 'selected' : ''}`}
                onClick={() => setSelectedNote(note)}
              >
                {note}
              </button>
            ))}
          </div>
        </div>

        <div className="control-group">
          <label htmlFor="scale-select">Scale Type:</label>
          <div className="scale-selector">
            {scaleTypes.map((scale) => (
              <button
                key={scale.value}
                className={`scale-btn ${selectedScaleType === scale.value ? 'selected' : ''}`}
                onClick={() => setSelectedScaleType(scale.value)}
              >
                {scale.label}
              </button>
            ))}
          </div>
        </div>

        <button className="search-btn" onClick={handleSearch}>
          Search Chords
        </button>
      </div>

      <div className="search-summary">
        <p>
          Searching for chords containing <strong>{selectedNote}</strong> in{' '}
          <strong>{selectedScaleType}</strong> scale context
        </p>
      </div>
    </div>
  );
};

export default NoteSearchInput;
