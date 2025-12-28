import React from 'react';
import './KeyToChordsView.css';

const KeyToChordsView: React.FC = () => {
  return (
    <div className="key-to-chords-view">
      <h2>Key Signature to Chords</h2>
      <p>Select a key signature to see diatonic chord suggestions.</p>
      <div className="placeholder">
        <p>This feature will be implemented in Phase 3</p>
        <ul>
          <li>Key signature selector</li>
          <li>Diatonic chord suggestions</li>
          <li>Music notation display</li>
        </ul>
      </div>
    </div>
  );
};

export default KeyToChordsView;
