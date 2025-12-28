import React, { useState } from 'react';
import KeySignatureInput from '../KeySignature/KeySignatureInput';
import ChordListInput from '../ChordInput/ChordListInput';
import ChordSubstitutionDisplay from '../ChordDisplay/ChordSubstitutionDisplay';
import ImprovisationNotesDisplay from '../NotesDisplay/ImprovisationNotesDisplay';
import chordService from '../../../services/chordService';
import {
  SubstitutionOption,
  ImprovisationNotesResponse,
} from '../../../types/chord';
import './ChordSubstitutionView.css';

type InputMode = 'key' | 'chords';
type Technique = 'random' | 'tritone' | 'diatonic' | 'chromatic' | 'circle-of-fifths';

const ChordSubstitutionView: React.FC = () => {
  const [inputMode, setInputMode] = useState<InputMode>('chords');
  const [selectedKey, setSelectedKey] = useState<string>('');
  const [selectedChords, setSelectedChords] = useState<string[]>([]);
  const [selectedTechnique, setSelectedTechnique] = useState<Technique>('random');
  const [currentChord, setCurrentChord] = useState<string>('');
  const [substitutions, setSubstitutions] = useState<SubstitutionOption[]>([]);
  const [improvisationNotes, setImprovisationNotes] =
    useState<ImprovisationNotesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleKeySignatureSelect = async (key: string) => {
    setSelectedKey(key);
    setError(null);
    try {
      setLoading(true);
      const chords = await chordService.getChordsByKey(key);
      const chordSymbols = chords.map((c) => c.symbol);
      setSelectedChords(chordSymbols);
    } catch (err) {
      setError('Failed to load chords for the selected key');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChordsChange = (chords: string[]) => {
    setSelectedChords(chords);
  };

  const handleGetSubstitutions = async (chord: string) => {
    if (!chord) return;

    setCurrentChord(chord);
    setError(null);

    try {
      setLoading(true);
      const response = await chordService.getSubstitutions(chord, selectedTechnique);
      setSubstitutions(response.substitutions);

      // Also get improvisation notes
      const notesResponse = await chordService.getImprovisationNotes(chord, 5);
      setImprovisationNotes(notesResponse);
    } catch (err) {
      setError('Failed to get substitutions and notes');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const techniques: { value: Technique; label: string; description: string }[] = [
    {
      value: 'random',
      label: 'Random',
      description: 'Random selection from available chords',
    },
    {
      value: 'tritone',
      label: 'Tritone Substitution',
      description: 'Replace with chord a tritone away',
    },
    {
      value: 'diatonic',
      label: 'Diatonic',
      description: 'Stay within the key signature',
    },
    {
      value: 'chromatic',
      label: 'Chromatic Approach',
      description: 'Use chromatic passing chords',
    },
    {
      value: 'circle-of-fifths',
      label: 'Circle of Fifths',
      description: 'Follow the circle of fifths progression',
    },
  ];

  return (
    <div className="chord-substitution-view">
      <div className="view-header">
        <h1>🎵 Chord Reharmonization & Improvisation</h1>
        <p className="subtitle">
          Discover new chord substitutions and improvisation notes for your music
        </p>
      </div>

      {/* Input Mode Selector */}
      <div className="input-mode-selector">
        <button
          className={`mode-btn ${inputMode === 'key' ? 'active' : ''}`}
          onClick={() => setInputMode('key')}
        >
          📝 Classical (Key Signature)
        </button>
        <button
          className={`mode-btn ${inputMode === 'chords' ? 'active' : ''}`}
          onClick={() => setInputMode('chords')}
        >
          🎸 Modern (Chord List)
        </button>
      </div>

      {/* Input Section */}
      <div className="input-section">
        {inputMode === 'key' ? (
          <KeySignatureInput onKeySignatureSelect={handleKeySignatureSelect} />
        ) : (
          <ChordListInput onChordsChange={handleChordsChange} />
        )}
      </div>

      {/* Technique Selector */}
      {selectedChords.length > 0 && (
        <div className="technique-selector">
          <h3>Substitution Technique</h3>
          <div className="technique-grid">
            {techniques.map((tech) => (
              <button
                key={tech.value}
                className={`technique-card ${
                  selectedTechnique === tech.value ? 'selected' : ''
                }`}
                onClick={() => setSelectedTechnique(tech.value)}
              >
                <div className="technique-label">{tech.label}</div>
                <div className="technique-description">{tech.description}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Chord Selection for Substitution */}
      {selectedChords.length > 0 && (
        <div className="chord-selection-section">
          <h3>Select a Chord to Reharmonize</h3>
          <div className="chord-buttons">
            {selectedChords.map((chord, index) => (
              <button
                key={index}
                className={`chord-select-btn ${currentChord === chord ? 'active' : ''}`}
                onClick={() => handleGetSubstitutions(chord)}
              >
                {chord}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading substitutions and improvisation notes...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="error-state">
          <p>⚠️ {error}</p>
        </div>
      )}

      {/* Results */}
      {!loading && currentChord && substitutions.length > 0 && (
        <div className="results-section">
          <ChordSubstitutionDisplay
            originalChord={currentChord}
            substitutions={substitutions}
            onSelectSubstitution={handleGetSubstitutions}
          />
        </div>
      )}

      {!loading && improvisationNotes && (
        <div className="results-section">
          <ImprovisationNotesDisplay notesData={improvisationNotes} />
        </div>
      )}
    </div>
  );
};

export default ChordSubstitutionView;
