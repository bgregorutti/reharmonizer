import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Chord } from '../types/chord';

interface ChordContextType {
  currentChords: Chord[];
  setCurrentChords: (chords: Chord[]) => void;
  selectedChord: Chord | null;
  setSelectedChord: (chord: Chord | null) => void;
}

const ChordContext = createContext<ChordContextType | undefined>(undefined);

export const ChordProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentChords, setCurrentChords] = useState<Chord[]>([]);
  const [selectedChord, setSelectedChord] = useState<Chord | null>(null);

  return (
    <ChordContext.Provider
      value={{
        currentChords,
        setCurrentChords,
        selectedChord,
        setSelectedChord,
      }}
    >
      {children}
    </ChordContext.Provider>
  );
};

export const useChordContext = () => {
  const context = useContext(ChordContext);
  if (!context) {
    throw new Error('useChordContext must be used within ChordProvider');
  }
  return context;
};
