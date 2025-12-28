import React from 'react';
import { ImprovisationNotesResponse } from '../../../types/chord';
import MusicNotation from '../../common/MusicNotation';
import './ImprovisationNotesDisplay.css';

interface ImprovisationNotesDisplayProps {
  notesData: ImprovisationNotesResponse;
}

const ImprovisationNotesDisplay: React.FC<ImprovisationNotesDisplayProps> = ({
  notesData,
}) => {
  const { chord_symbol, chord_tones, scale_notes, recommended_notes, avoid_notes } =
    notesData;

  return (
    <div className="improvisation-notes-display">
      <h3>Improvisation Notes for {chord_symbol}</h3>

      <div className="notes-sections">
        {/* Recommended Notes - Main focus */}
        <div className="notes-card recommended">
          <div className="card-header">
            <h4>🎵 Recommended Notes</h4>
            <span className="note-count">{recommended_notes.length} notes</span>
          </div>
          <div className="notes-notation">
            <MusicNotation notes={recommended_notes} width={500} height={150} />
          </div>
          <div className="notes-list">
            {recommended_notes.map((note, index) => (
              <span key={index} className="note-badge recommended-badge">
                {note}
              </span>
            ))}
          </div>
          <p className="card-description">
            These notes work best for improvisation over {chord_symbol}
          </p>
        </div>

        <div className="info-grid">
          {/* Chord Tones */}
          <div className="notes-card chord-tones">
            <div className="card-header">
              <h4>🎹 Chord Tones</h4>
              <span className="note-count">{chord_tones.length} notes</span>
            </div>
            <div className="notes-list">
              {chord_tones.map((note, index) => (
                <span key={index} className="note-badge chord-tone-badge">
                  {note}
                </span>
              ))}
            </div>
            <p className="card-description">
              The notes that make up the {chord_symbol} chord. These are safe and
              strong choices.
            </p>
          </div>

          {/* Scale Notes */}
          <div className="notes-card scale-notes">
            <div className="card-header">
              <h4>🎼 Scale Notes</h4>
              <span className="note-count">{scale_notes.length} notes</span>
            </div>
            <div className="notes-list">
              {scale_notes.map((note, index) => (
                <span key={index} className="note-badge scale-badge">
                  {note}
                </span>
              ))}
            </div>
            <p className="card-description">
              Notes from the appropriate scale. Great for melodic passages.
            </p>
          </div>

          {/* Avoid Notes */}
          {avoid_notes && avoid_notes.length > 0 && (
            <div className="notes-card avoid-notes">
              <div className="card-header">
                <h4>⚠️ Avoid Notes</h4>
                <span className="note-count">{avoid_notes.length} notes</span>
              </div>
              <div className="notes-list">
                {avoid_notes.map((note, index) => (
                  <span key={index} className="note-badge avoid-badge">
                    {note}
                  </span>
                ))}
              </div>
              <p className="card-description">
                These notes may clash with the chord. Use sparingly or as passing
                tones.
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="usage-tips">
        <h4>💡 Improvisation Tips</h4>
        <ul>
          <li>
            <strong>Start with chord tones</strong> - They outline the harmony clearly
          </li>
          <li>
            <strong>Add scale notes</strong> - Connect chord tones with melodic lines
          </li>
          <li>
            <strong>Use recommended notes</strong> - Our suggestions balance both for
            interesting phrases
          </li>
          <li>
            <strong>Avoid notes carefully</strong> - Can create tension if used as
            passing tones
          </li>
        </ul>
      </div>
    </div>
  );
};

export default ImprovisationNotesDisplay;
