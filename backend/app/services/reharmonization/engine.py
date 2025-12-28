"""
Reharmonization engine - coordinates chord substitution recommendations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from reharmonizer_core import ChordRecommender, NoteRecommender
from app.models.chord import Chord


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
        Recommend chord substitutions.

        Args:
            source_chord: Original chord symbol
            technique: Recommendation technique (random, tritone, diatonic, etc.)
            count: Number of recommendations

        Returns:
            List of chord recommendations with metadata
        """
        # Get available chords from database
        chords = self.db.query(Chord).all()

        # Convert to dict format for recommender
        available_chords = [
            {
                "symbol": chord.symbol,
                "root_note": chord.root_note,
                "notes": chord.notes,
                "intervals": chord.intervals,
                "chord_quality": chord.chord_quality,
            }
            for chord in chords
        ]

        # Get recommendations from core package
        recommendations = self.chord_recommender.recommend_by_technique(
            source_chord=source_chord,
            available_chords=available_chords,
            technique=technique,
            count=count,
        )

        # Add technique description to each recommendation
        technique_desc = self.chord_recommender.get_technique_description(technique)

        result = []
        for rec in recommendations:
            result.append(
                {
                    "chord": rec["symbol"],
                    "root_note": rec["root_note"],
                    "notes": rec["notes"],
                    "chord_quality": rec.get("chord_quality", "unknown"),
                    "technique": technique,
                    "description": technique_desc,
                    "score": 1.0,  # Placeholder - will be replaced with similarity score
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
