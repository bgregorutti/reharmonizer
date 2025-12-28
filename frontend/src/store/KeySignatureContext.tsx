import React, { createContext, useContext, useState, ReactNode } from 'react';
import { KeySignature } from '../types/keySignature';

interface KeySignatureContextType {
  currentKey: KeySignature | null;
  setCurrentKey: (key: KeySignature | null) => void;
}

const KeySignatureContext = createContext<KeySignatureContextType | undefined>(undefined);

export const KeySignatureProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentKey, setCurrentKey] = useState<KeySignature | null>(null);

  return (
    <KeySignatureContext.Provider
      value={{
        currentKey,
        setCurrentKey,
      }}
    >
      {children}
    </KeySignatureContext.Provider>
  );
};

export const useKeySignatureContext = () => {
  const context = useContext(KeySignatureContext);
  if (!context) {
    throw new Error('useKeySignatureContext must be used within KeySignatureProvider');
  }
  return context;
};
