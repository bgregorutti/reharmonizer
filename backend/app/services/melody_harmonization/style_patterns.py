"""
Style patterns - Genre-specific chord progression patterns.
"""

from typing import List, Dict, Any, Optional


class StylePatterns:
    """
    Manage and apply style-specific chord progression patterns.
    """

    # Common jazz patterns
    JAZZ_PATTERNS = [
        {
            "name": "ii-V-I",
            "pattern": ["ii7", "V7", "Imaj7"],
            "description": "Most common jazz progression",
            "usage": "Cadence, turnaround",
        },
        {
            "name": "I-vi-ii-V",
            "pattern": ["Imaj7", "vi7", "ii7", "V7"],
            "description": "Jazz turnaround",
            "usage": "End of phrases, repeated sections",
        },
        {
            "name": "Minor ii-V-i",
            "pattern": ["ii7b5", "V7", "im7"],
            "description": "Minor key ii-V-i",
            "usage": "Minor key cadence",
        },
        {
            "name": "Blues progression",
            "pattern": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"],
            "description": "12-bar blues",
            "usage": "Blues form",
        },
    ]

    # Common pop patterns
    POP_PATTERNS = [
        {
            "name": "I-V-vi-IV",
            "pattern": ["I", "V", "vi", "IV"],
            "description": "Most popular pop progression",
            "usage": "Verse, chorus",
        },
        {
            "name": "I-IV-V",
            "pattern": ["I", "IV", "V"],
            "description": "Classic pop progression",
            "usage": "Verse, chorus",
        },
        {
            "name": "vi-IV-I-V",
            "pattern": ["vi", "IV", "I", "V"],
            "description": "Popular alternative",
            "usage": "Verse, pre-chorus",
        },
        {
            "name": "I-vi-IV-V",
            "pattern": ["I", "vi", "IV", "V"],
            "description": "50s progression",
            "usage": "Verse",
        },
    ]

    # Common classical patterns
    CLASSICAL_PATTERNS = [
        {
            "name": "I-IV-V-I",
            "pattern": ["I", "IV", "V", "I"],
            "description": "Perfect cadence",
            "usage": "Phrase ending, strong resolution",
        },
        {
            "name": "I-ii-V-I",
            "pattern": ["I", "ii", "V", "I"],
            "description": "Subdominant approach",
            "usage": "Phrase structure",
        },
        {
            "name": "I-vi-ii-V",
            "pattern": ["I", "vi", "ii", "V"],
            "description": "Circle progression",
            "usage": "Extended phrases",
        },
        {
            "name": "I-IV-I-V",
            "pattern": ["I", "IV", "I", "V"],
            "description": "Simple functional harmony",
            "usage": "Basic phrase structure",
        },
    ]

    def __init__(self):
        """Initialize style patterns."""
        pass

    def get_patterns_for_style(self, style: str) -> List[Dict[str, Any]]:
        """
        Get chord progression patterns for a specific style.

        Args:
            style: Musical style ("jazz", "pop", "classical")

        Returns:
            List of pattern dictionaries
        """
        if style == "jazz":
            return self.JAZZ_PATTERNS
        elif style == "pop":
            return self.POP_PATTERNS
        elif style == "classical":
            return self.CLASSICAL_PATTERNS
        else:
            return []

    def convert_roman_to_chords(
        self, pattern: List[str], key_signature: str
    ) -> List[str]:
        """
        Convert Roman numeral pattern to actual chord symbols.

        Args:
            pattern: List of Roman numerals (e.g., ["I", "IV", "V"])
            key_signature: Key signature (e.g., "C major")

        Returns:
            List of chord symbols (e.g., ["C", "F", "G"])
        """
        # Parse key signature
        parts = key_signature.split()
        if len(parts) != 2:
            return []

        tonic = parts[0]
        mode = parts[1].lower()

        # Major scale mapping
        major_scale_map = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
            "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
            "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"],
            "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
            "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
        }

        if tonic not in major_scale_map:
            return []

        scale = major_scale_map[tonic]

        # Convert Roman numerals to chords
        result = []
        for numeral in pattern:
            chord_symbol = self._roman_to_chord(numeral, scale, mode)
            if chord_symbol:
                result.append(chord_symbol)

        return result

    def _roman_to_chord(self, numeral: str, scale: List[str], mode: str) -> str:
        """
        Convert a single Roman numeral to chord symbol.

        Args:
            numeral: Roman numeral (e.g., "I", "ii7", "V7")
            scale: Scale notes
            mode: "major" or "minor"

        Returns:
            Chord symbol (e.g., "Cmaj7", "Dm7")
        """
        # Parse the Roman numeral
        base = numeral.rstrip("0123456789b#")
        extensions = numeral[len(base) :]

        # Map Roman to scale degree (1-indexed)
        roman_map = {
            "I": 0,
            "i": 0,
            "II": 1,
            "ii": 1,
            "III": 2,
            "iii": 2,
            "IV": 3,
            "iv": 3,
            "V": 4,
            "v": 4,
            "VI": 5,
            "vi": 5,
            "VII": 6,
            "vii": 6,
        }

        # Handle flat/sharp modifiers
        modifier = ""
        if base.startswith("b"):
            modifier = "b"
            base = base[1:]
        elif base.startswith("#"):
            modifier = "#"
            base = base[1:]

        if base not in roman_map:
            return ""

        degree = roman_map[base]
        root = scale[degree]

        # Apply modifier
        if modifier == "b":
            # Flatten the note
            if root.endswith("#"):
                root = root[:-1]  # F# -> F
            elif root == "C":
                root = "Cb"
            elif root == "F":
                root = "E"
            elif root == "E":
                root = "Eb"
            else:
                root = root + "b"
        elif modifier == "#":
            # Sharpen the note
            if root.endswith("b"):
                root = root[:-1]  # Bb -> B
            elif root == "B":
                root = "B#"
            elif root == "E":
                root = "E#"
            else:
                root = root + "#"

        # Determine chord quality
        if mode == "major":
            # Major key qualities: I, ii, iii, IV, V, vi, vii°
            qualities = ["maj", "m", "m", "maj", "maj", "m", "dim"]
            quality = qualities[degree]
        else:
            # Minor key qualities: i, ii°, III, iv, v, VI, VII
            qualities = ["m", "dim", "maj", "m", "m", "maj", "maj"]
            quality = qualities[degree]

        # Build chord symbol
        chord = root

        # Add quality
        if quality == "m":
            chord += "m"
        elif quality == "dim":
            chord += "dim"
        # Major is default, no suffix needed

        # Add extensions
        if "maj7" in extensions or "Maj7" in extensions:
            chord += "maj7"
        elif "7" in extensions:
            if quality == "maj":
                chord += "7"  # Dominant 7th
            else:
                chord += "7"  # Minor 7th or diminished 7th
        elif "9" in extensions:
            chord += "9"

        # Handle special cases
        if "b5" in extensions:
            chord += "b5"

        return chord

    def apply_pattern_to_progression(
        self,
        chord_progression: List[str],
        style: str,
        key_signature: str,
    ) -> Dict[str, Any]:
        """
        Try to match and refine a chord progression to a known pattern.

        Args:
            chord_progression: List of chord symbols
            style: Musical style
            key_signature: Key signature

        Returns:
            Dictionary with refined progression and pattern info
        """
        patterns = self.get_patterns_for_style(style)

        # For now, just return the original progression
        # Future: implement pattern matching and refinement
        return {
            "chords": chord_progression,
            "pattern_applied": None,
            "pattern_name": None,
        }
