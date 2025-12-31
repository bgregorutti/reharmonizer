"""
Chord matcher - Match chords from database to melody notes.
"""

from typing import List, Dict, Any, Optional, Set
from sqlalchemy.orm import Session
from app.models.chord import Chord
from app.models.key_signature import KeySignature


class ChordMatcher:
    """
    Match chords from the database to melody notes based on music theory.
    """

    def __init__(self, db: Session):
        """
        Initialize the chord matcher.

        Args:
            db: Database session
        """
        self.db = db

    def find_chords_for_notes(
        self,
        pitch_classes: Set[str],
        key_signature: str,
        style: str = "jazz",
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Find chords from database that contain the given pitch classes.

        Args:
            pitch_classes: Set of pitch class names (e.g., {"C", "E", "G"})
            key_signature: Key signature (e.g., "C major")
            style: Musical style ("jazz", "pop", "classical")
            limit: Maximum number of chords to return

        Returns:
            List of chord dictionaries with scores
        """
        # Get key signature from database
        key_obj = self.db.query(KeySignature).filter_by(key_name=key_signature).first()

        if not key_obj:
            # Fallback: get all chords
            chords = self.db.query(Chord).all()
        else:
            # Get diatonic chords for this key
            chords = self.db.query(Chord).filter_by(key_signature_id=key_obj.id).all()

        # Score and filter chords
        scored_chords = []

        for chord in chords:
            score = self._score_chord(chord, pitch_classes, style)
            if score > 0:
                scored_chords.append(
                    {
                        "chord": chord,
                        "symbol": chord.symbol,
                        "root_note": chord.root_note,
                        "notes": chord.notes,
                        "chord_quality": chord.chord_quality,
                        "score": score,
                    }
                )

        # Sort by score (highest first)
        scored_chords.sort(key=lambda x: x["score"], reverse=True)

        # Apply style-specific filtering
        filtered_chords = self._apply_style_filter(scored_chords, style)

        return filtered_chords[:limit]

    def _score_chord(
        self, chord: Chord, pitch_classes: Set[str], style: str
    ) -> float:
        """
        Score how well a chord matches the given pitch classes.

        Args:
            chord: Chord object from database
            pitch_classes: Set of pitch classes from melody
            style: Musical style

        Returns:
            Score (0.0 to 1.0)
        """
        chord_notes = set(chord.notes) if chord.notes else set()

        if not chord_notes or not pitch_classes:
            return 0.0

        # Check if all melody notes are in the chord
        if pitch_classes.issubset(chord_notes):
            # All melody notes are in chord - excellent match
            base_score = 1.0
        else:
            # Some melody notes are not in chord
            # Score based on percentage of matching notes
            matching = pitch_classes.intersection(chord_notes)
            base_score = len(matching) / len(pitch_classes) if pitch_classes else 0.0

        # Adjust score based on style preferences
        style_bonus = 0.0

        if style == "jazz":
            # Prefer extended chords (7th, 9th, etc.)
            if "7" in chord.symbol or "9" in chord.symbol:
                style_bonus = 0.2
            elif "maj7" in chord.symbol:
                style_bonus = 0.15

        elif style == "pop":
            # Prefer simple triads and basic 7ths
            if chord.chord_quality in ["major", "minor"]:
                style_bonus = 0.2
            elif "7" not in chord.symbol:  # Triads
                style_bonus = 0.1

        elif style == "classical":
            # Prefer diatonic chords
            if chord.chord_quality in ["major", "minor", "diminished"]:
                style_bonus = 0.15

        return min(base_score + style_bonus, 1.0)

    def _apply_style_filter(
        self, scored_chords: List[Dict[str, Any]], style: str
    ) -> List[Dict[str, Any]]:
        """
        Filter chords based on style preferences.

        Args:
            scored_chords: List of scored chord dictionaries
            style: Musical style

        Returns:
            Filtered list of chords
        """
        if style == "jazz":
            # Prefer 7th chords and extensions
            filtered = [
                c
                for c in scored_chords
                if "7" in c["symbol"] or "9" in c["symbol"] or "maj7" in c["symbol"]
            ]
            # If not enough, add others
            if len(filtered) < 5:
                filtered.extend([c for c in scored_chords if c not in filtered])
            return filtered

        elif style == "pop":
            # Prefer triads and simple chords
            filtered = [
                c
                for c in scored_chords
                if c["chord_quality"] in ["major", "minor"]
                or ("7" not in c["symbol"] and "9" not in c["symbol"])
            ]
            if len(filtered) < 5:
                filtered.extend([c for c in scored_chords if c not in filtered])
            return filtered

        elif style == "classical":
            # Prefer diatonic chords (major, minor, diminished)
            filtered = [
                c
                for c in scored_chords
                if c["chord_quality"] in ["major", "minor", "diminished"]
            ]
            if len(filtered) < 5:
                filtered.extend([c for c in scored_chords if c not in filtered])
            return filtered

        return scored_chords

    def select_best_chord(
        self,
        candidates: List[Dict[str, Any]],
        previous_chord: Optional[str] = None,
        next_chord: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Select the best chord from candidates considering context.

        Args:
            candidates: List of candidate chord dictionaries
            previous_chord: Previous chord symbol (for voice leading)
            next_chord: Next chord symbol (for progression logic)

        Returns:
            Best chord dictionary or None
        """
        if not candidates:
            return None

        # For now, return the highest scored chord
        # Future enhancement: consider voice leading and progression logic
        return candidates[0]

    def harmonize_phrase(
        self,
        phrase_notes: List[Dict[str, Any]],
        key_signature: str,
        style: str = "jazz",
    ) -> List[Dict[str, Any]]:
        """
        Harmonize a phrase by finding the best chord for its pitch content.

        Args:
            phrase_notes: List of note dictionaries in the phrase
            key_signature: Key signature
            style: Musical style

        Returns:
            List of chord recommendations for the phrase
        """
        # Extract pitch classes from phrase
        pitch_classes = set(
            n["pitch_class"] for n in phrase_notes if n.get("pitch_class")
        )

        if not pitch_classes:
            return []

        # Find matching chords
        matching_chords = self.find_chords_for_notes(
            pitch_classes, key_signature, style, limit=5
        )

        return matching_chords
