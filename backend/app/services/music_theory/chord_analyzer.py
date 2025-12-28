"""
Chord analyzer service - wraps reharmonizer_core functionality.

This module provides a bridge between the FastAPI backend and the reharmonizer-core package.
"""

from reharmonizer_core.theory import ChordAnalyzer as CoreChordAnalyzer
from typing import List, Dict, Any


class ChordAnalyzer:
    """
    Chord analyzer service.

    Wraps the reharmonizer_core.ChordAnalyzer for use in the backend.
    """

    def __init__(self):
        self.core_analyzer = CoreChordAnalyzer()

    def get_chord_tones(self, chord_symbol: str) -> List[str]:
        """Get notes that make up the chord."""
        return self.core_analyzer.get_chord_tones(chord_symbol)

    def get_chord_intervals(self, chord_symbol: str) -> List[int]:
        """Get intervals from root in semitones."""
        return self.core_analyzer.get_chord_intervals(chord_symbol)

    def get_chord_quality(self, chord_symbol: str) -> str:
        """Determine the chord quality."""
        return self.core_analyzer.get_chord_quality(chord_symbol)

    def analyze_voice_leading(self, chord1: str, chord2: str) -> Dict[str, Any]:
        """Analyze voice leading between two chords."""
        return self.core_analyzer.analyze_voice_leading(chord1, chord2)

    def get_shared_notes(self, chord1: str, chord2: str) -> List[str]:
        """Get notes shared between two chords."""
        return self.core_analyzer.get_shared_notes(chord1, chord2)
