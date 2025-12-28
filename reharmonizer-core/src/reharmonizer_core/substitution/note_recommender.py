"""
Note recommendation algorithm.

Provides note suggestions for improvisation based on a given chord.
"""

import random
from typing import List, Dict, Any
from music21 import chord as m21_chord, scale as m21_scale


class NoteRecommender:
    """
    Recommends notes for improvisation over a given chord.

    Extracts chord tones and scale notes, then provides recommendations.
    Current implementation uses simple random selection.
    """

    def __init__(self):
        """Initialize the note recommender."""
        pass

    def recommend_notes(
        self,
        chord_symbol: str,
        count: int = 5,
    ) -> Dict[str, Any]:
        """
        Recommend notes for improvisation over a chord.

        Args:
            chord_symbol: The chord symbol (e.g., "Cmaj7", "G7", "Dm")
            count: Number of note recommendations to return (default: 5)

        Returns:
            Dictionary containing:
                - chord_tones: Notes that make up the chord
                - scale_notes: Notes from the appropriate scale
                - recommended_notes: Random selection of suggested notes for improvisation
                - avoid_notes: Notes to avoid (if applicable)

        Example:
            >>> recommender = NoteRecommender()
            >>> result = recommender.recommend_notes("Cmaj7")
            >>> "chord_tones" in result
            True
            >>> "C" in result["chord_tones"]
            True
        """
        try:
            # Parse the chord using music21
            chord = m21_chord.Chord(chord_symbol)

            # Extract chord tones
            chord_tones = [p.name for p in chord.pitches]

            # Determine the appropriate scale
            root = chord.root().name
            scale_notes = self._get_scale_for_chord(chord, root)

            # Combine chord tones and scale notes for potential recommendations
            all_notes = list(set(chord_tones + scale_notes))

            # Randomly select notes for recommendations
            # Prefer chord tones and scale notes
            recommended_count = min(count, len(all_notes))
            recommended_notes = random.sample(all_notes, recommended_count)

            # Determine avoid notes (simplified)
            avoid_notes = self._get_avoid_notes(chord)

            return {
                "chord_symbol": chord_symbol,
                "chord_tones": chord_tones,
                "scale_notes": scale_notes,
                "recommended_notes": recommended_notes,
                "avoid_notes": avoid_notes,
            }

        except Exception as e:
            # If chord parsing fails, return empty result
            return {
                "chord_symbol": chord_symbol,
                "chord_tones": [],
                "scale_notes": [],
                "recommended_notes": [],
                "avoid_notes": [],
                "error": str(e),
            }

    def _get_scale_for_chord(self, chord: m21_chord.Chord, root: str) -> List[str]:
        """
        Determine the appropriate scale for a chord.

        Args:
            chord: music21 Chord object
            root: Root note name

        Returns:
            List of note names in the scale
        """
        try:
            # Determine scale based on chord quality
            if chord.isMajorTriad() or chord.isMajorSeventh():
                # Use major scale
                scale = m21_scale.MajorScale(root)
            elif chord.isMinorTriad() or chord.isMinorSeventh():
                # Use minor scale (natural minor)
                scale = m21_scale.MinorScale(root)
            elif chord.isDominantSeventh():
                # Use mixolydian scale (major scale with b7)
                scale = m21_scale.MixolydianScale(root)
            elif chord.isDiminishedTriad() or chord.isDiminishedSeventh():
                # Use diminished scale or whole-half
                # For simplicity, use locrian
                scale = m21_scale.LocrianScale(root)
            else:
                # Default to major scale
                scale = m21_scale.MajorScale(root)

            # Get unique note names (remove octave duplicates)
            notes = [p.name for p in scale.pitches]
            # Remove duplicates while preserving order
            seen = set()
            unique_notes = []
            for note in notes:
                if note not in seen:
                    seen.add(note)
                    unique_notes.append(note)

            return unique_notes

        except Exception:
            # If scale generation fails, return chromatic scale from root
            chromatic = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            # Rotate to start from root
            try:
                root_index = chromatic.index(root)
                return chromatic[root_index:] + chromatic[:root_index]
            except ValueError:
                return chromatic

    def _get_avoid_notes(self, chord: m21_chord.Chord) -> List[str]:
        """
        Determine avoid notes for the chord.

        Args:
            chord: music21 Chord object

        Returns:
            List of note names to avoid

        Note:
            Simplified implementation. Common avoid notes:
            - In major chords: the 4th (conflicts with major 3rd)
            - In minor chords: the 6th can be an avoid note
        """
        avoid = []

        try:
            root = chord.root()

            # For major chords, the 4th is typically an avoid note
            if chord.isMajorTriad() or chord.isMajorSeventh():
                # Calculate the 4th
                fourth_pitch = root.transpose("P4")  # Perfect 4th
                avoid.append(fourth_pitch.name)

            # For dominant 7th chords, avoid notes depend on context
            # For simplicity, we'll return empty for dominant chords

        except Exception:
            pass

        return avoid

    def get_note_function(self, note: str, chord_symbol: str) -> str:
        """
        Determine the function of a note in relation to a chord.

        Args:
            note: Note name (e.g., "G")
            chord_symbol: Chord symbol (e.g., "Cmaj7")

        Returns:
            Function description (e.g., "chord tone", "scale tone", "chromatic")

        Note:
            This is a simplified implementation.
        """
        result = self.recommend_notes(chord_symbol, count=10)

        if note in result.get("chord_tones", []):
            return "chord tone"
        elif note in result.get("scale_notes", []):
            return "scale tone"
        elif note in result.get("avoid_notes", []):
            return "avoid note"
        else:
            return "chromatic"
