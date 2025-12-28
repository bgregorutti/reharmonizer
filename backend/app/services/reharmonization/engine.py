"""
Reharmonization engine - coordinates chord substitution recommendations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from reharmonizer_core import ChordRecommender, NoteRecommender
from app.models.chord import Chord
from app.models.chord_substitution import ChordSubstitution


class ReharmonizationEngine:
    """
    Central engine that coordinates chord substitution and note recommendations.

    Uses the reharmonizer-core package for the actual recommendation algorithms.
    """

    def __init__(self, db: Session):
        """
        Initialize the reharmonization engine.

        Args:
            db: Database session for accessing chord data
        """
        self.db = db
        self.chord_recommender = ChordRecommender()
        self.note_recommender = NoteRecommender()

    def recommend_chord_substitutions(
        self,
        source_chord: str,
        technique: str = "random",
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Recommend chord substitutions using database-stored music theory relationships.

        Args:
            source_chord: Original chord symbol
            technique: Recommendation technique (random, tritone, diatonic, etc.)
            count: Number of recommendations

        Returns:
            List of chord recommendations with metadata
        """
        # Get the source chord from database
        source = self.db.query(Chord).filter(Chord.symbol == source_chord).first()

        if not source:
            # Fallback: source chord not found
            return []

        # Query substitutions from database
        query = (
            self.db.query(ChordSubstitution, Chord)
            .join(Chord, ChordSubstitution.target_chord_id == Chord.id)
            .filter(ChordSubstitution.source_chord_id == source.id)
        )

        # Filter by technique if specified and not "random"
        if technique and technique != "random":
            query = query.filter(ChordSubstitution.technique == technique)

        # Order by score (best substitutions first)
        query = query.order_by(ChordSubstitution.score.desc())

        # Get results
        substitutions = query.all()

        # If we have no results with the specific technique, try all techniques
        if not substitutions and technique != "random":
            query = (
                self.db.query(ChordSubstitution, Chord)
                .join(Chord, ChordSubstitution.target_chord_id == Chord.id)
                .filter(ChordSubstitution.source_chord_id == source.id)
                .order_by(ChordSubstitution.score.desc())
            )
            substitutions = query.all()

        # If still no results, fallback to random selection
        if not substitutions:
            return self._fallback_random_substitutions(source_chord, count)

        # Limit to requested count
        substitutions = substitutions[:count]

        # Format results
        result = []
        for sub, target_chord in substitutions:
            result.append(
                {
                    "chord": target_chord.symbol,
                    "root_note": target_chord.root_note,
                    "notes": target_chord.notes,
                    "chord_quality": target_chord.chord_quality,
                    "technique": sub.technique,
                    "description": sub.description,
                    "score": sub.score,
                    "usage_context": sub.usage_context,
                    "relationship_type": sub.relationship_type,
                }
            )

        return result

    def _fallback_random_substitutions(
        self, source_chord: str, count: int
    ) -> List[Dict[str, Any]]:
        """
        Fallback method for random substitutions when no theory-based substitutions exist.

        Args:
            source_chord: Original chord symbol
            count: Number of recommendations

        Returns:
            List of random chord recommendations
        """
        # Get available chords from database
        chords = (
            self.db.query(Chord)
            .filter(Chord.symbol != source_chord)
            .order_by(func.random())
            .limit(count)
            .all()
        )

        # Format results
        result = []
        for chord in chords:
            result.append(
                {
                    "chord": chord.symbol,
                    "root_note": chord.root_note,
                    "notes": chord.notes,
                    "chord_quality": chord.chord_quality,
                    "technique": "random",
                    "description": "Random selection (no music theory relationship found)",
                    "score": 0.5,
                }
            )

        return result

    def recommend_improvisation_notes(
        self, chord_symbol: str, count: int = 5
    ) -> Dict[str, Any]:
        """
        Recommend notes for improvisation over a chord.

        Args:
            chord_symbol: Chord symbol
            count: Number of note recommendations

        Returns:
            Dictionary with chord tones, scale notes, and recommendations
        """
        return self.note_recommender.recommend_notes(chord_symbol, count)

    def reharmonize_progression(
        self,
        chords: List[str],
        key_signature: Optional[str] = None,
        techniques: List[str] = ["random"],
        complexity: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Reharmonize a chord progression.

        Args:
            chords: Original chord progression
            key_signature: Optional key context
            techniques: List of techniques to use
            complexity: Complexity level (1-5)

        Returns:
            List of reharmonization suggestions
        """
        suggestions = []

        for technique in techniques:
            # For each technique, create a reharmonized version
            reharmonized_chords = []

            for chord in chords:
                # Get substitution for this chord
                subs = self.recommend_chord_substitutions(
                    source_chord=chord, technique=technique, count=1
                )

                if subs:
                    reharmonized_chords.append(subs[0]["chord"])
                else:
                    # If no substitution found, keep original
                    reharmonized_chords.append(chord)

            suggestions.append(
                {
                    "chords": reharmonized_chords,
                    "technique": technique,
                    "score": 0.8,  # Placeholder
                    "analysis": {
                        "technique_description": self.chord_recommender.get_technique_description(
                            technique
                        ),
                        "complexity": complexity,
                    },
                }
            )

        return suggestions
