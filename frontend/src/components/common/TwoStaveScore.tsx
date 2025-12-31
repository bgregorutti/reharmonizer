import React, { useEffect, useRef } from 'react';
import {
  Renderer,
  Stave,
  StaveNote,
  Voice,
  Formatter,
  Accidental,
  StaveConnector,
  Annotation,
} from 'vexflow';
import type { MelodyNote, ChordTiming } from '../../types/melody';
import './TwoStaveScore.css';

interface TwoStaveScoreProps {
  melodyNotes: MelodyNote[];
  chordTiming: ChordTiming[];
  width?: number;
  height?: number;
  timeSignature?: string;
  keySignature?: string;
}

const TwoStaveScore: React.FC<TwoStaveScoreProps> = ({
  melodyNotes,
  chordTiming,
  width = 900,
  height = 400,
  timeSignature = '4/4',
  keySignature = 'C',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    try {
      // Clear previous rendering
      containerRef.current.innerHTML = '';

      // Validate data
      if (melodyNotes.length === 0 || chordTiming.length === 0) {
        containerRef.current.innerHTML =
          '<div style="padding: 20px; text-align: center; color: #666;">No music data to display</div>';
        return;
      }

      // Create renderer
      const renderer = new Renderer(
        containerRef.current,
        Renderer.Backends.SVG
      );
      renderer.resize(width, height);
      const context = renderer.getContext();

      // Process melody notes into measures
      const melodyMeasures = groupNotesByMeasure(melodyNotes);

      // Process chords with timing
      const chordMeasures = distributeChordsByMeasure(chordTiming);

      // Determine how many measures to render (first 4 measures for now)
      const totalMeasures = Math.max(
        Object.keys(melodyMeasures).length,
        Object.keys(chordMeasures).length
      );
      const measuresToRender = Math.min(totalMeasures, 4);

      // Calculate stave positions
      const staveWidth = (width - 100) / measuresToRender;
      const trebleY = 40;
      const bassY = 180;

      // Render each measure
      for (let measureNum = 1; measureNum <= measuresToRender; measureNum++) {
        const x = 50 + (measureNum - 1) * staveWidth;

        // Create treble stave (melody)
        const trebleStave = new Stave(x, trebleY, staveWidth);
        trebleStave.addClef('treble');

        // Add time signature on first measure
        if (measureNum === 1) {
          trebleStave.addTimeSignature(timeSignature);
        }

        trebleStave.setContext(context).draw();

        // Create bass stave (chords)
        const bassStave = new Stave(x, bassY, staveWidth);
        bassStave.addClef('bass');

        if (measureNum === 1) {
          bassStave.addTimeSignature(timeSignature);
        }

        bassStave.setContext(context).draw();

        // Connect staves with brace on first measure
        if (measureNum === 1) {
          const connector = new StaveConnector(trebleStave, bassStave);
          connector.setType(StaveConnector.type.BRACE);
          connector.setContext(context).draw();
        }

        // Render melody notes for this measure
        const melodyNotesForMeasure = melodyMeasures[measureNum] || [];
        if (melodyNotesForMeasure.length > 0) {
          const melodyVexNotes = buildMelodyVoiceNotes(melodyNotesForMeasure);
          if (melodyVexNotes.length > 0) {
            const melodyVoice = new Voice({ num_beats: 4, beat_value: 4 });
            melodyVoice.setStrict(false);
            melodyVoice.addTickables(melodyVexNotes);

            new Formatter()
              .joinVoices([melodyVoice])
              .format([melodyVoice], staveWidth - 20);

            melodyVoice.draw(context, trebleStave);
          }
        } else {
          // Render rest if no melody
          const rest = new StaveNote({
            keys: ['b/4'],
            duration: 'wr',
            clef: 'treble',
          });
          const restVoice = new Voice({ num_beats: 4, beat_value: 4 });
          restVoice.setStrict(false);
          restVoice.addTickables([rest]);
          restVoice.draw(context, trebleStave);
        }

        // Render chords for this measure
        const chordsForMeasure = chordMeasures[measureNum] || [];
        if (chordsForMeasure.length > 0) {
          const chordVexNotes = buildChordVoiceNotes(chordsForMeasure);
          if (chordVexNotes.length > 0) {
            const chordVoice = new Voice({ num_beats: 4, beat_value: 4 });
            chordVoice.setStrict(false);
            chordVoice.addTickables(chordVexNotes);

            new Formatter()
              .joinVoices([chordVoice])
              .format([chordVoice], staveWidth - 20);

            chordVoice.draw(context, bassStave);
          }
        } else {
          // Render rest if no chord
          const rest = new StaveNote({
            keys: ['d/3'],
            duration: 'wr',
            clef: 'bass',
          });
          const restVoice = new Voice({ num_beats: 4, beat_value: 4 });
          restVoice.setStrict(false);
          restVoice.addTickables([rest]);
          restVoice.draw(context, bassStave);
        }
      }
    } catch (error) {
      console.error('VexFlow two-stave rendering error:', error);
      if (containerRef.current) {
        containerRef.current.innerHTML =
          '<div style="padding: 20px; text-align: center; color: #f44336;">Error rendering score</div>';
      }
    }
  }, [melodyNotes, chordTiming, width, height, timeSignature, keySignature]);

  return <div ref={containerRef} className="two-stave-score" />;
};

// Helper function: Group melody notes by measure
function groupNotesByMeasure(
  notes: MelodyNote[]
): Record<number, MelodyNote[]> {
  const measures: Record<number, MelodyNote[]> = {};

  notes.forEach((note) => {
    if (note.measure !== null && !note.is_rest) {
      if (!measures[note.measure]) {
        measures[note.measure] = [];
      }
      measures[note.measure].push(note);
    }
  });

  return measures;
}

// Helper function: Distribute chords by measure based on timing
function distributeChordsByMeasure(
  chordTiming: ChordTiming[]
): Record<number, ChordTiming[]> {
  const measures: Record<number, ChordTiming[]> = {};

  chordTiming.forEach((chord) => {
    if (chord.measure !== null) {
      if (!measures[chord.measure]) {
        measures[chord.measure] = [];
      }
      measures[chord.measure].push(chord);
    }
  });

  return measures;
}

// Build melody voice notes for VexFlow
function buildMelodyVoiceNotes(measureNotes: MelodyNote[]): StaveNote[] {
  const notes: StaveNote[] = [];

  measureNotes.forEach((note) => {
    try {
      const vexDuration = convertDurationToVexFlow(note.duration);
      const vexPitch = convertPitchToVexFlow(note.pitch || 'C4');

      const staveNote = new StaveNote({
        keys: [vexPitch],
        duration: vexDuration,
        clef: 'treble',
      });

      // Add accidentals
      if (note.pitch?.includes('#')) {
        staveNote.addModifier(new Accidental('#'), 0);
      } else if (note.pitch?.includes('b')) {
        staveNote.addModifier(new Accidental('b'), 0);
      }

      notes.push(staveNote);
    } catch (error) {
      console.error('Error building melody note:', error);
    }
  });

  return notes;
}

// Build chord voice notes with timing awareness
function buildChordVoiceNotes(measureChords: ChordTiming[]): StaveNote[] {
  const notes: StaveNote[] = [];

  measureChords.forEach((chord) => {
    try {
      const vexDuration = convertDurationToVexFlow(chord.duration);
      const chordNotes = parseChordToNotesForBass(chord.symbol);

      const staveNote = new StaveNote({
        keys: chordNotes,
        duration: vexDuration,
        clef: 'bass',
      });

      // Add chord symbol annotation above the chord
      staveNote.addModifier(
        new Annotation(chord.symbol)
          .setVerticalJustification(Annotation.VerticalJustify.TOP)
          .setFont('Arial', 12, 'bold'),
        0
      );

      // Add accidentals
      chordNotes.forEach((noteStr, index) => {
        if (noteStr.includes('#')) {
          staveNote.addModifier(new Accidental('#'), index);
        } else if (noteStr.includes('b')) {
          staveNote.addModifier(new Accidental('b'), index);
        }
      });

      notes.push(staveNote);
    } catch (error) {
      console.error('Error building chord note:', error);
    }
  });

  return notes;
}

// Convert duration (quarter notes) to VexFlow duration string
function convertDurationToVexFlow(quarterNotes: number): string {
  if (quarterNotes >= 4) return 'w'; // Whole note
  if (quarterNotes >= 2) return 'h'; // Half note
  if (quarterNotes >= 1) return 'q'; // Quarter note
  if (quarterNotes >= 0.5) return '8'; // Eighth note
  return '16'; // Sixteenth note
}

// Convert pitch string to VexFlow format
function convertPitchToVexFlow(pitch: string): string {
  if (!pitch) return 'c/4';

  // Extract note and octave
  const match = pitch.match(/^([A-G][#b]?)(\d+)$/);
  if (!match) return 'c/4';

  const [, note, octave] = match;
  return `${note.toLowerCase()}/${octave}`;
}

// Parse chord symbol to bass clef notes (close voicing, middle register)
function parseChordToNotesForBass(chordSymbol: string): string[] {
  // Extract root
  const rootMatch = chordSymbol.match(/^([A-G][#b]?)/);
  if (!rootMatch) return ['c/3', 'e/3', 'g/3'];

  const root = rootMatch[1];
  const quality = chordSymbol.replace(root, '').toLowerCase();

  // Start from octave 3 for bass clef (middle register, close voicing)
  const baseNote = convertPitchToVexFlow(`${root}3`);

  // Use voicing logic based on chord quality
  if (quality === '' || quality === 'maj' || quality === 'major') {
    // Major: root, major third, perfect fifth
    return [baseNote, transposeNote(baseNote, 4), transposeNote(baseNote, 7)];
  } else if (
    quality === 'm' ||
    quality === 'min' ||
    quality === 'minor' ||
    quality === '-'
  ) {
    // Minor: root, minor third, perfect fifth
    return [baseNote, transposeNote(baseNote, 3), transposeNote(baseNote, 7)];
  } else if (quality === '7' || quality === 'dom7') {
    // Dominant 7: root, third, fifth, minor seventh
    return [
      baseNote,
      transposeNote(baseNote, 4),
      transposeNote(baseNote, 7),
      transposeNote(baseNote, 10),
    ];
  } else if (quality === 'maj7') {
    // Major 7: root, third, fifth, major seventh
    return [
      baseNote,
      transposeNote(baseNote, 4),
      transposeNote(baseNote, 7),
      transposeNote(baseNote, 11),
    ];
  } else if (quality === 'm7' || quality === 'min7') {
    // Minor 7: root, minor third, fifth, minor seventh
    return [
      baseNote,
      transposeNote(baseNote, 3),
      transposeNote(baseNote, 7),
      transposeNote(baseNote, 10),
    ];
  } else if (quality === 'dim' || quality === '°') {
    // Diminished: root, minor third, diminished fifth
    return [baseNote, transposeNote(baseNote, 3), transposeNote(baseNote, 6)];
  } else if (quality === 'aug' || quality === '+') {
    // Augmented: root, major third, augmented fifth
    return [baseNote, transposeNote(baseNote, 4), transposeNote(baseNote, 8)];
  } else {
    // Default to major triad
    return [baseNote, transposeNote(baseNote, 4), transposeNote(baseNote, 7)];
  }
}

// Transpose helper (reuse from MusicNotation.tsx)
function transposeNote(vfNote: string, semitones: number): string {
  try {
    const noteMap = [
      'c',
      'c#',
      'd',
      'd#',
      'e',
      'f',
      'f#',
      'g',
      'g#',
      'a',
      'a#',
      'b',
    ];

    const [notePart, octave] = vfNote.split('/');
    if (!notePart || !octave) return 'c/3';

    let currentNote = notePart.replace('b', '#');
    const currentIndex = noteMap.indexOf(currentNote);
    if (currentIndex === -1) return vfNote;

    let newIndex = (currentIndex + semitones) % 12;
    if (newIndex < 0) newIndex += 12;

    let newOctave =
      parseInt(octave) + Math.floor((currentIndex + semitones) / 12);

    return `${noteMap[newIndex]}/${newOctave}`;
  } catch (error) {
    console.error(`Error transposing note ${vfNote}:`, error);
    return 'c/3';
  }
}

export default TwoStaveScore;
