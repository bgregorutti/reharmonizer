"""
Chord progression patterns model - Store common chord progression patterns.
"""

from sqlalchemy import Column, Integer, String, JSON, Float, Text
from sqlalchemy.sql import func
from app.database import Base


class ChordProgressionPattern(Base):
    """
    Store common chord progression patterns for different musical styles.
    """

    __tablename__ = "chord_progression_patterns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # "ii-V-I", "I-V-vi-IV", etc.
    style = Column(String(20), nullable=False, index=True)  # "jazz", "pop", "classical"

    # Roman numeral sequence for pattern matching
    roman_numeral_sequence = Column(JSON, nullable=False)  # ["ii", "V", "I"]

    # Example chord sequence (for reference)
    example_chords = Column(JSON)  # ["Dm7", "G7", "Cmaj7"]

    # Pattern metadata
    description = Column(Text)
    usage_context = Column(Text)  # "Cadence", "Turnaround", "Verse", etc.
    popularity_score = Column(Float, default=0.5)  # 0.0 to 1.0

    # Pattern properties
    min_length = Column(Integer, default=2)  # Minimum chords in pattern
    max_length = Column(Integer, default=12)  # Maximum chords in pattern
    is_repeatable = Column(Integer, default=0)  # Can this pattern repeat?

    def __repr__(self):
        return f"<ChordProgressionPattern(name='{self.name}', style='{self.style}')>"
