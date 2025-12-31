"""
Melody analyzer - Analyze melody for key detection, phrase segmentation, etc.
"""

from typing import List, Dict, Any, Optional


class MelodyAnalyzer:
    """
    Analyze melody to detect key, segment into phrases, and extract musical features.
    """

    def __init__(self):
        """Initialize the melody analyzer."""
        pass

    def segment_into_phrases(
        self, melody_notes: List[Dict[str, Any]], min_rest_duration: float = 1.0
    ) -> List[List[Dict[str, Any]]]:
        """
        Segment melody into phrases based on rests and long notes.

        Args:
            melody_notes: List of note dictionaries
            min_rest_duration: Minimum rest duration to trigger phrase boundary

        Returns:
            List of phrases, where each phrase is a list of notes
        """
        phrases = []
        current_phrase = []

        for i, note_dict in enumerate(melody_notes):
            # Check for phrase boundary
            is_boundary = False

            # Rest-based boundary
            if note_dict["is_rest"] and note_dict["duration"] >= min_rest_duration:
                is_boundary = True

            # Long note at end of phrase (followed by rest or significant gap)
            if (
                not note_dict["is_rest"]
                and note_dict["duration"] >= 2.0
                and i < len(melody_notes) - 1
            ):
                next_note = melody_notes[i + 1]
                if next_note["is_rest"] or (
                    next_note["offset"] - (note_dict["offset"] + note_dict["duration"])
                    > 0.5
                ):
                    current_phrase.append(note_dict)
                    is_boundary = True

            if is_boundary:
                if current_phrase:
                    phrases.append(current_phrase)
                    current_phrase = []
            else:
                if not note_dict["is_rest"]:  # Don't include rests in phrases
                    current_phrase.append(note_dict)

        # Add remaining phrase
        if current_phrase:
            phrases.append(current_phrase)

        # If no phrases were created, treat entire melody as one phrase
        if not phrases:
            phrases.append([n for n in melody_notes if not n["is_rest"]])

        return phrases

    def analyze_phrase(self, phrase: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a single phrase to extract musical features.

        Args:
            phrase: List of note dictionaries

        Returns:
            Dictionary with phrase analysis:
            {
                "pitch_classes": Set of unique pitch classes,
                "duration": Total duration,
                "start_offset": Starting offset,
                "end_offset": Ending offset,
                "num_notes": Number of notes,
                "contour": Melodic contour (ascending/descending/static)
            }
        """
        if not phrase:
            return {
                "pitch_classes": set(),
                "duration": 0.0,
                "start_offset": 0.0,
                "end_offset": 0.0,
                "num_notes": 0,
                "contour": "static",
            }

        # Extract pitch classes
        pitch_classes = set(n["pitch_class"] for n in phrase if n["pitch_class"])

        # Calculate duration and offsets
        start_offset = phrase[0]["offset"]
        end_offset = phrase[-1]["offset"] + phrase[-1]["duration"]
        duration = end_offset - start_offset

        # Analyze contour
        contour = self._analyze_contour(phrase)

        return {
            "pitch_classes": pitch_classes,
            "duration": duration,
            "start_offset": start_offset,
            "end_offset": end_offset,
            "num_notes": len(phrase),
            "contour": contour,
        }

    def _analyze_contour(self, phrase: List[Dict[str, Any]]) -> str:
        """
        Analyze the melodic contour of a phrase.

        Args:
            phrase: List of note dictionaries

        Returns:
            "ascending", "descending", "static", or "mixed"
        """
        if len(phrase) < 2:
            return "static"

        # Get MIDI values
        midi_values = [n["midi"] for n in phrase if n["midi"] is not None]

        if len(midi_values) < 2:
            return "static"

        # Calculate differences
        differences = [midi_values[i + 1] - midi_values[i] for i in range(len(midi_values) - 1)]

        ascending = sum(1 for d in differences if d > 0)
        descending = sum(1 for d in differences if d < 0)
        static = sum(1 for d in differences if d == 0)

        # Determine predominant direction
        total = len(differences)
        if ascending > total * 0.6:
            return "ascending"
        elif descending > total * 0.6:
            return "descending"
        elif static > total * 0.6:
            return "static"
        else:
            return "mixed"

    def get_chord_change_points(
        self, melody_notes: List[Dict[str, Any]], measures_per_chord: int = 1
    ) -> List[float]:
        """
        Determine optimal points for chord changes based on melody structure.

        Args:
            melody_notes: List of note dictionaries
            measures_per_chord: Default number of measures per chord

        Returns:
            List of offsets where chords should change
        """
        change_points = []

        # Group notes by measure
        measures = {}
        for note_dict in melody_notes:
            if note_dict["is_rest"]:
                continue
            measure = note_dict["measure"]
            if measure not in measures:
                measures[measure] = []
            measures[measure].append(note_dict)

        # Create change points at regular intervals
        sorted_measures = sorted(measures.keys())

        for i in range(0, len(sorted_measures), measures_per_chord):
            measure_num = sorted_measures[i]
            if measures[measure_num]:
                # Use the offset of the first note in the measure
                change_points.append(measures[measure_num][0]["offset"])

        return change_points

    def detect_harmonic_rhythm(
        self, melody_notes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Detect the harmonic rhythm (how often chords should change).

        Args:
            melody_notes: List of note dictionaries

        Returns:
            Dictionary with harmonic rhythm analysis
        """
        # Analyze note durations and phrase structure
        phrases = self.segment_into_phrases(melody_notes)

        avg_phrase_duration = (
            sum(self.analyze_phrase(p)["duration"] for p in phrases) / len(phrases)
            if phrases
            else 4.0
        )

        # Determine appropriate chord density
        if avg_phrase_duration <= 2.0:
            # Short phrases - change chords frequently
            recommendation = "high"
            measures_per_chord = 0.5
        elif avg_phrase_duration <= 4.0:
            # Medium phrases - moderate chord changes
            recommendation = "medium"
            measures_per_chord = 1
        else:
            # Long phrases - fewer chord changes
            recommendation = "low"
            measures_per_chord = 2

        return {
            "density": recommendation,
            "measures_per_chord": measures_per_chord,
            "avg_phrase_duration": avg_phrase_duration,
            "num_phrases": len(phrases),
        }
