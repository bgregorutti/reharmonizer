"""
Enhanced harmonization engine using chord progression patterns.
"""

from typing import List, Dict, Any, Set, Optional
from sqlalchemy.orm import Session
from app.models.chord_progression import ChordProgressionPattern
from app.services.melody_harmonization import (
    MelodyAnalyzer,
    ChordMatcher,
    StylePatterns,
)


class EnhancedHarmonizationEngine:
    """
    Enhanced harmonization engine that uses chord progression patterns
    to generate musically coherent harmonizations.
    """

    def __init__(self, db: Session):
        """
        Initialize the enhanced harmonization engine.

        Args:
            db: Database session
        """
        self.db = db
        self.analyzer = MelodyAnalyzer()
        self.chord_matcher = ChordMatcher(db)
        self.style_patterns = StylePatterns()

    def harmonize(
        self,
        melody_notes: List[Dict[str, Any]],
        key_signature: str,
        style: str = "jazz",
        num_alternatives: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple harmonization options for a melody.

        Args:
            melody_notes: List of note dictionaries
            key_signature: Key signature (e.g., "C major")
            style: Musical style ("jazz", "pop", "classical")
            num_alternatives: Number of alternative harmonizations to generate

        Returns:
            List of harmonization results, each with chord progression and metadata
        """
        # Determine harmonic rhythm (how often chords should change)
        harmonic_rhythm = self.analyzer.detect_harmonic_rhythm(melody_notes)

        # Get change points for chords
        change_points = self.analyzer.get_chord_change_points(
            melody_notes, measures_per_chord=harmonic_rhythm["measures_per_chord"]
        )

        # Generate primary harmonization using patterns
        primary = self._harmonize_with_patterns(
            melody_notes, key_signature, style, change_points
        )

        # Generate alternatives
        alternatives = []
        alternatives.append(primary)

        # Alternative 1: Direct chord matching (original method)
        alt1 = self._harmonize_direct_matching(
            melody_notes, key_signature, style, change_points
        )
        alternatives.append(alt1)

        # Alternative 2: Use different pattern if available
        if num_alternatives > 2:
            alt2 = self._harmonize_with_patterns(
                melody_notes, key_signature, style, change_points, variant=1
            )
            alternatives.append(alt2)

        return alternatives[:num_alternatives]

    def _harmonize_with_patterns(
        self,
        melody_notes: List[Dict[str, Any]],
        key_signature: str,
        style: str,
        change_points: List[float],
        variant: int = 0,
    ) -> Dict[str, Any]:
        """
        Harmonize using chord progression patterns from database.

        Args:
            melody_notes: List of note dictionaries
            key_signature: Key signature
            style: Musical style
            change_points: List of offsets where chords should change
            variant: Pattern variant to use (0 = most popular, 1 = second most, etc.)

        Returns:
            Harmonization result dictionary
        """
        # Get appropriate patterns for this style
        patterns = (
            self.db.query(ChordProgressionPattern)
            .filter_by(style=style)
            .order_by(ChordProgressionPattern.popularity_score.desc())
            .all()
        )

        if not patterns:
            # Fallback to direct matching if no patterns available
            return self._harmonize_direct_matching(
                melody_notes, key_signature, style, change_points
            )

        # Select pattern based on number of chord changes needed
        num_changes = len(change_points)
        selected_pattern = self._select_best_pattern(patterns, num_changes, variant)

        if not selected_pattern:
            return self._harmonize_direct_matching(
                melody_notes, key_signature, style, change_points
            )

        # Convert pattern to actual chords
        pattern_chords = self.style_patterns.convert_roman_to_chords(
            selected_pattern.roman_numeral_sequence, key_signature
        )

        # If pattern is repeatable and we need more chords, repeat it
        chord_progression = []
        chord_details = []

        if selected_pattern.is_repeatable and len(pattern_chords) < num_changes:
            # Repeat pattern to fill all change points
            while len(chord_progression) < num_changes:
                chord_progression.extend(pattern_chords)
            chord_progression = chord_progression[:num_changes]
        else:
            # Use pattern as is, or truncate if too long
            chord_progression = pattern_chords[:num_changes]

        # Get details for each chord
        for chord_symbol in chord_progression:
            # Find chord in database
            matching = self.chord_matcher.find_chords_for_notes(
                pitch_classes=set(),  # Find by symbol, not by notes
                key_signature=key_signature,
                style=style,
                limit=10,
            )

            # Find exact match by symbol
            chord_detail = None
            for match in matching:
                if match["symbol"] == chord_symbol:
                    chord_detail = match
                    break

            # If not found, use first match or create placeholder
            if not chord_detail and matching:
                chord_detail = matching[0]
                chord_detail["symbol"] = chord_symbol  # Override symbol

            if chord_detail:
                chord_details.append(chord_detail)

        # Calculate timing information for chords
        chord_timing = self._calculate_chord_timing(
            chord_progression, change_points, melody_notes
        )

        return {
            "chord_progression": chord_progression,
            "chord_details": chord_details,
            "chord_timing": chord_timing,
            "pattern_name": selected_pattern.name,
            "pattern_description": selected_pattern.description,
            "score": selected_pattern.popularity_score,
            "method": "pattern_based",
        }

    def _harmonize_direct_matching(
        self,
        melody_notes: List[Dict[str, Any]],
        key_signature: str,
        style: str,
        change_points: List[float],
    ) -> Dict[str, Any]:
        """
        Harmonize by directly matching chords to melody notes (original method).

        Args:
            melody_notes: List of note dictionaries
            key_signature: Key signature
            style: Musical style
            change_points: List of offsets where chords should change

        Returns:
            Harmonization result dictionary
        """
        # Segment melody based on change points
        segments = self._segment_by_change_points(melody_notes, change_points)

        chord_progression = []
        chord_details = []

        for segment in segments:
            if not segment:
                continue

            # Extract pitch classes from segment
            pitch_classes = set(
                n["pitch_class"] for n in segment if n.get("pitch_class")
            )

            if not pitch_classes:
                continue

            # Find matching chords
            matching_chords = self.chord_matcher.find_chords_for_notes(
                pitch_classes, key_signature, style, limit=5
            )

            if matching_chords:
                best_chord = self.chord_matcher.select_best_chord(matching_chords)
                if best_chord:
                    chord_progression.append(best_chord["symbol"])
                    chord_details.append(best_chord)

        # Calculate average score
        avg_score = (
            sum(c.get("score", 0.5) for c in chord_details) / len(chord_details)
            if chord_details
            else 0.5
        )

        # Calculate timing information for chords
        chord_timing = self._calculate_chord_timing(
            chord_progression, change_points, melody_notes
        )

        return {
            "chord_progression": chord_progression,
            "chord_details": chord_details,
            "chord_timing": chord_timing,
            "pattern_name": None,
            "pattern_description": "Direct melody-to-chord matching",
            "score": avg_score,
            "method": "direct_matching",
        }

    def _select_best_pattern(
        self,
        patterns: List[ChordProgressionPattern],
        num_changes: int,
        variant: int = 0,
    ) -> Optional[ChordProgressionPattern]:
        """
        Select the best chord progression pattern for the given number of changes.

        Args:
            patterns: List of available patterns
            num_changes: Number of chord changes needed
            variant: Which variant to select (0 = best, 1 = second best, etc.)

        Returns:
            Selected pattern or None
        """
        # Filter patterns that can work for this number of changes
        suitable_patterns = []

        for pattern in patterns:
            pattern_length = len(pattern.roman_numeral_sequence)

            # Pattern is suitable if:
            # 1. It's the exact length we need, OR
            # 2. It's repeatable and can be repeated to fit, OR
            # 3. It's longer and can be truncated
            if pattern_length == num_changes:
                suitable_patterns.append((pattern, 1.0))  # Perfect match
            elif pattern.is_repeatable and pattern_length <= num_changes:
                # Can repeat - score based on how well it divides
                repetitions = num_changes / pattern_length
                fit_score = 1.0 if repetitions == int(repetitions) else 0.7
                suitable_patterns.append((pattern, fit_score))
            elif pattern_length > num_changes and pattern_length <= num_changes * 2:
                # Can truncate - slight penalty
                suitable_patterns.append((pattern, 0.6))

        if not suitable_patterns:
            # If no suitable patterns, just use the most popular one
            return patterns[variant] if variant < len(patterns) else patterns[0]

        # Sort by fit score, then by popularity
        suitable_patterns.sort(
            key=lambda x: (x[1] * x[0].popularity_score), reverse=True
        )

        # Select variant
        if variant < len(suitable_patterns):
            return suitable_patterns[variant][0]
        else:
            return suitable_patterns[0][0] if suitable_patterns else None

    def _segment_by_change_points(
        self, melody_notes: List[Dict[str, Any]], change_points: List[float]
    ) -> List[List[Dict[str, Any]]]:
        """
        Segment melody into chunks based on change points.

        Args:
            melody_notes: List of note dictionaries
            change_points: List of offsets where segments should start

        Returns:
            List of note segments
        """
        segments = []
        current_segment = []

        change_point_idx = 0
        next_change = (
            change_points[change_point_idx] if change_points else float("inf")
        )

        for note in melody_notes:
            if note["is_rest"]:
                continue

            # Check if we've reached a change point
            if note["offset"] >= next_change:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []

                # Move to next change point
                change_point_idx += 1
                next_change = (
                    change_points[change_point_idx]
                    if change_point_idx < len(change_points)
                    else float("inf")
                )

            current_segment.append(note)

        # Add remaining segment
        if current_segment:
            segments.append(current_segment)

        return segments

    def _calculate_chord_timing(
        self,
        chord_progression: List[str],
        change_points: List[float],
        melody_notes: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Calculate timing information for each chord in the progression.

        Args:
            chord_progression: List of chord symbols
            change_points: List of offsets where chords change
            melody_notes: Original melody notes for measure lookup

        Returns:
            List of chord timing dictionaries with symbol, measure, offset, and duration
        """
        chord_timings = []

        for i, chord_symbol in enumerate(chord_progression):
            start_offset = change_points[i]

            # Calculate duration (until next change point or end of melody)
            if i < len(change_points) - 1:
                duration = change_points[i + 1] - start_offset
            else:
                # Last chord - calculate to end of melody
                last_note = melody_notes[-1]
                end_offset = last_note["offset"] + last_note["duration"]
                duration = end_offset - start_offset

            # Find measure number for this offset
            measure = None
            for note in melody_notes:
                if note["offset"] >= start_offset and not note["is_rest"]:
                    measure = note["measure"]
                    break

            # Default to measure 1 if not found
            if measure is None:
                measure = 1

            chord_timings.append({
                "symbol": chord_symbol,
                "measure": measure,
                "offset": start_offset,
                "duration": duration,
            })

        return chord_timings
