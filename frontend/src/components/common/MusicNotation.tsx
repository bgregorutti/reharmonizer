import React, { useEffect, useRef } from 'react';
import { Renderer, Stave, StaveNote, Voice, Formatter, Accidental } from 'vexflow';

interface MusicNotationProps {
  chords?: string[];
  notes?: string[];
  width?: number;
  height?: number;
}

const MusicNotation: React.FC<MusicNotationProps> = ({
  chords = [],
  notes = [],
  width = 600,
  height = 200,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Clear previous content
    containerRef.current.innerHTML = '';

    // Create renderer
    const renderer = new Renderer(
      containerRef.current,
      Renderer.Backends.SVG
    );
    renderer.resize(width, height);
    const context = renderer.getContext();

    // Create stave
    const stave = new Stave(10, 40, width - 20);
    stave.addClef('treble');
    stave.setContext(context).draw();

    // Convert chords or notes to VexFlow notes
    const vfNotes: StaveNote[] = [];

    if (chords.length > 0) {
      // Render chords
      chords.forEach((chord) => {
        const chordNotes = parseChordToNotes(chord);
        const staveNote = new StaveNote({
          keys: chordNotes,
          duration: 'q',
        });

        // Add accidentals if needed
        chordNotes.forEach((note, index) => {
          if (note.includes('#')) {
            staveNote.addModifier(new Accidental('#'), index);
          } else if (note.includes('b')) {
            staveNote.addModifier(new Accidental('b'), index);
          }
        });

        vfNotes.push(staveNote);
      });
    } else if (notes.length > 0) {
      // Render individual notes
      notes.forEach((note) => {
        const vfNote = noteToVexFlowFormat(note);
        const staveNote = new StaveNote({
          keys: [vfNote],
          duration: 'q',
        });

        // Add accidentals
        if (note.includes('#')) {
          staveNote.addModifier(new Accidental('#'), 0);
        } else if (note.includes('b')) {
          staveNote.addModifier(new Accidental('b'), 0);
        }

        vfNotes.push(staveNote);
      });
    }

    // If we have notes to render
    if (vfNotes.length > 0) {
      const voice = new Voice({ num_beats: vfNotes.length, beat_value: 4 });
      voice.addTickables(vfNotes);

      new Formatter().joinVoices([voice]).format([voice], width - 50);

      voice.draw(context, stave);
    }
  }, [chords, notes, width, height]);

  return (
    <div
      ref={containerRef}
      className="music-notation"
      style={{ border: '1px solid #ddd', borderRadius: '4px', padding: '10px' }}
    />
  );
};

// Helper function to convert chord symbol to VexFlow note format
function parseChordToNotes(chordSymbol: string): string[] {
  // Extract root note from chord symbol
  const rootMatch = chordSymbol.match(/^([A-G][#b]?)/);
  if (!rootMatch) return ['c/4'];

  const root = rootMatch[1];
  const vfRoot = noteToVexFlowFormat(root);

  // Determine chord quality and build chord notes
  const quality = chordSymbol.replace(root, '').toLowerCase();

  // Basic chord voicings (root position, close voicing in treble clef)
  if (quality === '' || quality === 'maj' || quality === 'major') {
    // Major triad: root, third, fifth
    return [vfRoot, transposeNote(vfRoot, 4), transposeNote(vfRoot, 7)];
  } else if (quality === 'm' || quality === 'min' || quality === 'minor') {
    // Minor triad: root, minor third, fifth
    return [vfRoot, transposeNote(vfRoot, 3), transposeNote(vfRoot, 7)];
  } else if (quality === '7' || quality === 'dom7') {
    // Dominant 7th: root, third, fifth, minor seventh
    return [
      vfRoot,
      transposeNote(vfRoot, 4),
      transposeNote(vfRoot, 7),
      transposeNote(vfRoot, 10),
    ];
  } else if (quality === 'maj7') {
    // Major 7th: root, third, fifth, major seventh
    return [
      vfRoot,
      transposeNote(vfRoot, 4),
      transposeNote(vfRoot, 7),
      transposeNote(vfRoot, 11),
    ];
  } else if (quality === 'm7' || quality === 'min7') {
    // Minor 7th: root, minor third, fifth, minor seventh
    return [
      vfRoot,
      transposeNote(vfRoot, 3),
      transposeNote(vfRoot, 7),
      transposeNote(vfRoot, 10),
    ];
  } else {
    // Default to major triad for unknown qualities
    return [vfRoot, transposeNote(vfRoot, 4), transposeNote(vfRoot, 7)];
  }
}

// Convert note name (e.g., "C", "C#", "Db") to VexFlow format (e.g., "c/4")
function noteToVexFlowFormat(note: string): string {
  const noteName = note[0].toLowerCase();
  const accidental = note.slice(1);

  // Default to 4th octave for display
  return `${noteName}${accidental}/4`;
}

// Transpose a VexFlow note by semitones
function transposeNote(vfNote: string, semitones: number): string {
  const noteMap = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b'];
  const flatMap = ['c', 'db', 'd', 'eb', 'e', 'f', 'gb', 'g', 'ab', 'a', 'bb', 'b'];

  const [notePart, octave] = vfNote.split('/');
  let currentNote = notePart.replace('b', '#'); // Normalize flats to sharps

  const currentIndex = noteMap.indexOf(currentNote);
  if (currentIndex === -1) return vfNote;

  let newIndex = (currentIndex + semitones) % 12;
  let newOctave = parseInt(octave) + Math.floor((currentIndex + semitones) / 12);

  // Use sharps by default, but could be enhanced to choose based on key
  const newNote = noteMap[newIndex];

  return `${newNote}/${newOctave}`;
}

export default MusicNotation;
