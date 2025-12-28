"""
Chord recommendation algorithm.

Provides chord substitution suggestions based on the input chord.
Current implementation uses simple random selection from available chords.
"""

import random
from typing import List, Dict, Any, Optional


class ChordRecommender:
    """
    Recommends alternative chords for substitution.

    Current implementation: Simple random selection from available chords.
    Future: Will use similarity scoring based on shared notes, intervals, and harmonic function.
    """

    def __init__(self):
        """Initialize the chord recommender."""
        pass

    def recommend_chords(
        self,
        source_chord: str,
        available_chords: List[Dict[str, Any]],
        count: int = 5,
        exclude_source: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Recommend alternative chords for substitution.

        Args:
            source_chord: The original chord symbol (e.g., "C7")
            available_chords: List of chord dictionaries from database
                Each dict should have: {symbol, root_note, notes, intervals, chord_quality}
            count: Number of recommendations to return (default: 5)
            exclude_source: Whether to exclude the source chord from recommendations

        Returns:
            List of recommended chord dictionaries (up to 'count' chords)

        Example:
            >>> recommender = ChordRecommender()
            >>> chords = [
            ...     {"symbol": "C7", "root_note": "C", "notes": ["C", "E", "G", "Bb"]},
            ...     {"symbol": "Db7", "root_note": "Db", "notes": ["Db", "F", "Ab", "Cb"]},
            ...     {"symbol": "Em", "root_note": "E", "notes": ["E", "G", "B"]},
            ... ]
            >>> suggestions = recommender.recommend_chords("C7", chords, count=2)
            >>> len(suggestions) <= 2
            True
        """
        # Filter out the source chord if requested
        candidates = available_chords
        if exclude_source:
            candidates = [
                chord for chord in available_chords if chord.get("symbol") != source_chord
            ]

        # If we don't have enough candidates, return what we have
        if len(candidates) <= count:
            return candidates

        # Randomly select 'count' chords
        # Note: This is a simple implementation. Future versions will use similarity scoring.
        return random.sample(candidates, count)

    def recommend_by_technique(
        self,
        source_chord: str,
        available_chords: List[Dict[str, Any]],
        technique: str = "random",
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Recommend chords using a specific technique.

        Args:
            source_chord: The original chord symbol
            available_chords: List of available chords
            technique: Recommendation technique ("random", "tritone", "diatonic", etc.)
            count: Number of recommendations

        Returns:
            List of recommended chords

        Note:
            Currently only "random" technique is implemented.
            Future versions will implement:
            - tritone: Tritone substitution (dominant chords a tritone apart)
            - diatonic: Same scale degree in different keys
            - chromatic: Chromatic approach chords
            - circle_fifths: Circle of fifths relationships
        """
        if technique == "random":
            return self.recommend_chords(source_chord, available_chords, count)

        # Placeholder for future techniques
        # For now, fall back to random
        return self.recommend_chords(source_chord, available_chords, count)

    def get_technique_description(self, technique: str) -> str:
        """
        Get a description of a substitution technique.

        Args:
            technique: The technique name

        Returns:
            Human-readable description of the technique
        """
        descriptions = {
            "random": "Random selection from available chords",
            "tritone": "Tritone substitution (dominant 7th chord a tritone away)",
            "diatonic": "Chords from the same diatonic scale",
            "chromatic": "Chromatic approach chords",
            "circle_fifths": "Circle of fifths progressions",
        }
        return descriptions.get(technique, "Unknown technique")
