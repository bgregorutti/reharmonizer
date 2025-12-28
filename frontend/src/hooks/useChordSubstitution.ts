import { useState, useCallback } from 'react';
import { chordService } from '../services/chordService';
import { SubstitutionRequest, SubstitutionResponse } from '../types/chord';

export const useChordSubstitution = () => {
  const [suggestions, setSuggestions] = useState<SubstitutionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSubstitutions = useCallback(async (request: SubstitutionRequest) => {
    setLoading(true);
    setError(null);

    try {
      const response = await chordService.getSubstitutions(request);
      setSuggestions(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    suggestions,
    loading,
    error,
    fetchSubstitutions,
  };
};
