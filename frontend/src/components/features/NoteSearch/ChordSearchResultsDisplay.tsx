import React, { useEffect, useRef } from 'react';
import { Renderer, Stave, StaveNote, Voice, Formatter, Accidental } from 'vexflow';
import { Chord } from '../../../types/chord';
import './ChordSearchResultsDisplay.css';

interface ChordSearchResultsDisplayProps {
  searchedNote: string;
  scaleType: string;
  chords: Chord[];
}

const ChordSearchResultsDisplay: React.FC<ChordSearchResultsDisplayProps> = ({
  searchedNote,
  scaleType,
  chords,
}) => {
  const rendererRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  useEffect(() => {
    // Render VexFlow notation for each chord
    chords.forEach((chord) => {
      const container = rendererRefs.current[chord.symbol];
      if (!container) return;

      // Clear previous content
      container.innerHTML = '';

      try {
        const renderer = new Renderer(container, Renderer.Backends.SVG);

        // Configure and resize
        renderer.resize(200, 150);
        const context = renderer.getContext();

        // Validate chord has notes
        if (!chord.notes || chord.notes.length === 0) {
          throw new Error('No notes in chord');
        }

        // Create a stave
        const stave = new Stave(10, 10, 180);
        stave.addClef('treble');
        stave.setContext(context).draw();

        // Convert notes to VexFlow format
        // VexFlow requires notes in ascending order from bottom to top
        const noteOrder = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];

        const notesWithOctaves = chord.notes.map((note, index) => {
          // Normalize note for VexFlow (E- -> Eb)
          const baseNote = note.trim().replace('-', 'b').replace(/[0-9]/g, '');

          // Validate note
          if (!baseNote || baseNote.length === 0) {
            throw new Error(`Invalid note: ${note}`);
          }

          const noteLetter = baseNote.charAt(0).toUpperCase();

          // Validate note letter
          if (!noteOrder.includes(noteLetter)) {
            throw new Error(`Invalid note letter: ${noteLetter} from ${note}`);
          }

          // Assign octaves based on note position in the chord
          // Start at octave 4 and increase as needed
          let octave = 4;
          if (index === 0) octave = 4;
          else if (index === 1) octave = 4;
          else if (index === 2) octave = 4;
          else octave = 5;

          return {
            original: note,
            vexNote: baseNote,
            octave,
            fullNote: `${baseNote}/${octave}`,
            noteIndex: noteOrder.indexOf(noteLetter),
          };
        });

        // Sort notes by octave and then by note position
        notesWithOctaves.sort((a, b) => {
          if (a.octave !== b.octave) return a.octave - b.octave;
          return a.noteIndex - b.noteIndex;
        });

        const vexNotes = notesWithOctaves.map((n) => n.fullNote);

        // Create a chord note (all notes at once)
        const chordNote = new StaveNote({
          keys: vexNotes,
          duration: 'w', // whole note
        });

        // Add accidentals for sharps and flats (based on sorted order)
        notesWithOctaves.forEach((noteObj, index) => {
          if (noteObj.original.includes('#')) {
            chordNote.addModifier(new Accidental('#'), index);
          } else if (noteObj.original.includes('-')) {
            chordNote.addModifier(new Accidental('b'), index);
          }
        });

        // Create a voice and add the note
        const voice = new Voice({ num_beats: 4, beat_value: 4 });
        voice.addTickable(chordNote);

        // Format and draw
        new Formatter().joinVoices([voice]).format([voice], 150);
        voice.draw(context, stave);
      } catch (error) {
        console.error(`Error rendering chord ${chord.symbol}:`, error);
        console.error('Chord notes:', chord.notes);
        container.innerHTML = `<p class="render-error">Unable to render notation<br/><small>${error instanceof Error ? error.message : 'Unknown error'}</small></p>`;
      }
    });
  }, [chords]);

  return (
    <div className="chord-search-results">
      <div className="results-header">
        <h2>
          Chords containing <span className="highlight-note">{searchedNote}</span>
        </h2>
        <p className="results-context">
          {chords.length} chord{chords.length !== 1 ? 's' : ''} found in{' '}
          <strong>{scaleType}</strong> scale context
        </p>
      </div>

      <div className="chords-grid">
        {chords.map((chord) => (
          <div key={chord.id} className="chord-card">
            <div className="chord-header">
              <h3 className="chord-symbol">{chord.symbol}</h3>
              <span className={`chord-quality-badge ${chord.chord_quality}`}>
                {chord.chord_quality}
              </span>
            </div>

            <div
              className="chord-notation"
              ref={(el) => (rendererRefs.current[chord.symbol] = el)}
            />

            <div className="chord-info">
              <div className="info-row">
                <span className="info-label">Root:</span>
                <span className="info-value">{chord.root_note}</span>
              </div>
              <div className="info-row">
                <span className="info-label">Notes:</span>
                <span className="info-value notes-list">
                  {chord.notes.map((note, index) => (
                    <span
                      key={index}
                      className={`note ${note.replace('-', 'b') === searchedNote.replace('-', 'b') ? 'searched-note' : ''}`}
                    >
                      {note}
                    </span>
                  ))}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChordSearchResultsDisplay;
