import React from 'react';
import './ChordToNotesView.css';

const ChordToNotesView: React.FC = () => {
  return (
    <div className="chord-to-notes-view">
      <h2>Chord to Notes - Improvisation Helper</h2>
      <p>Enter a chord to see available notes for improvisation.</p>
      <div className="placeholder">
        <p>This feature will be implemented in Phase 5</p>
        <ul>
          <li>Chord input</li>
          <li>Chord tones display</li>
          <li>Scale notes for the chord</li>
          <li>Available tensions</li>
          <li>Avoid notes</li>
          <li>Music notation display</li>
        </ul>
      </div>
    </div>
  );
};

export default ChordToNotesView;
