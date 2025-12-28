"""
Reharmonizer Core - Music theory and chord substitution algorithms.

This package provides the core music theory logic used by the Reharmonizer application.
"""

__version__ = "0.1.0"

from reharmonizer_core.substitution.chord_recommender import ChordRecommender
from reharmonizer_core.substitution.note_recommender import NoteRecommender

__all__ = [
    "ChordRecommender",
    "NoteRecommender",
]
