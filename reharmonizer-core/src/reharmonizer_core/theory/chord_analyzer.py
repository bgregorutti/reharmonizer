"""Chord analysis utilities."""

from typing import List, Dict, Any
from music21 import chord as m21_chord, interval as m21_interval


class ChordAnalyzer:
    """Analyze chord properties and relationships."""

    @staticmethod
    def get_chord_tones(chord_symbol: str) -> List[str]:
        """
        Get notes that make up the chord.

        Args:
            chord_symbol: Chord symbol (e.g., "Cmaj7")

        Returns:
            List of note names
        """
        try:
            chord = m21_chord.Chord(chord_symbol)
            return [p.name for p in chord.pitches]
        except Exception:
            return []

    @staticmethod
    def get_chord_intervals(chord_symbol: str) -> List[int]:
        """
        Get intervals from root in semitones.

        Args:
            chord_symbol: Chord symbol

        Returns:
            List of intervals in semitones
        """
        try:
            chord = m21_chord.Chord(chord_symbol)
            root = chord.root()
            return [p.midi - root.midi for p in chord.pitches]
        except Exception:
            return []

    @staticmethod
    def get_chord_quality(chord_symbol: str) -> str:
        """
        Determine the chord quality.

        Args:
            chord_symbol: Chord symbol

        Returns:
            Quality string (e.g., "major7", "minor", "dominant7")
        """
        try:
            chord = m21_chord.Chord(chord_symbol)

            if chord.isDominantSeventh():
                return "dominant7"
            elif chord.isMajorSeventh():
                return "major7"
            elif chord.isMinorSeventh():
                return "minor7"
            elif chord.isDiminishedSeventh():
                return "diminished7"
            elif chord.isHalfDiminishedSeventh():
                return "half-diminished7"
            elif chord.isMajorTriad():
                return "major"
            elif chord.isMinorTriad():
                return "minor"
            elif chord.isDiminishedTriad():
                return "diminished"
            elif chord.isAugmentedTriad():
                return "augmented"
            else:
                return "other"

        except Exception:
            return "unknown"

    @staticmethod
    def analyze_voice_leading(chord1_symbol: str, chord2_symbol: str) -> Dict[str, Any]:
        """
        Analyze voice leading between two chords.

        Args:
            chord1_symbol: First chord symbol
            chord2_symbol: Second chord symbol

        Returns:
            Dictionary with voice leading analysis
        """
        try:
            chord1 = m21_chord.Chord(chord1_symbol)
            chord2 = m21_chord.Chord(chord2_symbol)

            movements = []
            for p1 in chord1.pitches:
                # Find closest pitch in chord2
                min_distance = float("inf")
                for p2 in chord2.pitches:
                    distance = abs(m21_interval.Interval(p1, p2).semitones)
                    if distance < min_distance:
                        min_distance = distance
                movements.append(min_distance)

            return {
                "average_movement": sum(movements) / len(movements) if movements else 0,
                "max_movement": max(movements) if movements else 0,
                "total_movement": sum(movements),
                "smooth": max(movements) <= 2 if movements else False,  # Stepwise motion
            }

        except Exception as e:
            return {
                "average_movement": 0,
                "max_movement": 0,
                "total_movement": 0,
                "smooth": False,
                "error": str(e),
            }

    @staticmethod
    def get_shared_notes(chord1_symbol: str, chord2_symbol: str) -> List[str]:
        """
        Get notes shared between two chords.

        Args:
            chord1_symbol: First chord symbol
            chord2_symbol: Second chord symbol

        Returns:
            List of shared note names
        """
        try:
            notes1 = set(ChordAnalyzer.get_chord_tones(chord1_symbol))
            notes2 = set(ChordAnalyzer.get_chord_tones(chord2_symbol))
            return list(notes1.intersection(notes2))
        except Exception:
            return []
