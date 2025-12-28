"""Wrapper around music21 for common conversions."""

from typing import Dict, Any
from music21 import chord as m21_chord, key as m21_key


class Music21Converter:
    """Convert between music21 objects and simple data structures."""

    @staticmethod
    def chord_to_dict(chord_symbol: str) -> Dict[str, Any]:
        """
        Convert chord symbol to dictionary.

        Args:
            chord_symbol: Chord symbol (e.g., "Cmaj7")

        Returns:
            Dictionary with chord information
        """
        try:
            chord = m21_chord.Chord(chord_symbol)

            # Determine quality
            if chord.isDominantSeventh():
                quality = "dominant7"
            elif chord.isMajorSeventh():
                quality = "major7"
            elif chord.isMinorSeventh():
                quality = "minor7"
            elif chord.isMajorTriad():
                quality = "major"
            elif chord.isMinorTriad():
                quality = "minor"
            else:
                quality = "other"

            return {
                "symbol": chord_symbol,
                "root_note": chord.root().name,
                "notes": [p.name for p in chord.pitches],
                "intervals": [p.midi - chord.root().midi for p in chord.pitches],
                "chord_quality": quality,
            }

        except Exception as e:
            return {
                "symbol": chord_symbol,
                "root_note": "",
                "notes": [],
                "intervals": [],
                "chord_quality": "unknown",
                "error": str(e),
            }

    @staticmethod
    def key_to_dict(key_name: str, mode: str = "major") -> Dict[str, Any]:
        """
        Convert key signature to dictionary.

        Args:
            key_name: Key name (e.g., "C", "G")
            mode: "major" or "minor"

        Returns:
            Dictionary with key signature information
        """
        try:
            if mode.lower() == "major":
                key = m21_key.Key(key_name)
            else:
                key = m21_key.Key(key_name, "minor")

            return {
                "key_name": f"{key_name} {mode}",
                "tonic": key_name,
                "mode": mode,
                "sharps_flats": key.sharps,  # Positive for sharps, negative for flats
                "scale_notes": [p.name for p in key.pitches],
            }

        except Exception as e:
            return {
                "key_name": f"{key_name} {mode}",
                "tonic": key_name,
                "mode": mode,
                "sharps_flats": 0,
                "scale_notes": [],
                "error": str(e),
            }
