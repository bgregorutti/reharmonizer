"""
Music21 integration wrapper - bridges music21 and our data models.
"""

from reharmonizer_core.music21_integration import Music21Converter as CoreConverter
from typing import Dict, Any


class Music21Converter:
    """
    Wrapper around reharmonizer_core.Music21Converter.

    Provides conversion between music21 objects and our data structures.
    """

    def __init__(self):
        self.core_converter = CoreConverter()

    def chord_to_dict(self, chord_symbol: str) -> Dict[str, Any]:
        """
        Convert chord symbol to dictionary.

        Args:
            chord_symbol: Chord symbol (e.g., "Cmaj7")

        Returns:
            Dictionary with chord information
        """
        return self.core_converter.chord_to_dict(chord_symbol)

    def key_to_dict(self, key_name: str, mode: str = "major") -> Dict[str, Any]:
        """
        Convert key signature to dictionary.

        Args:
            key_name: Key name (e.g., "C", "G")
            mode: "major" or "minor"

        Returns:
            Dictionary with key signature information
        """
        return self.core_converter.key_to_dict(key_name, mode)
