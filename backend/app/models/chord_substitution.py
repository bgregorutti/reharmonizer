from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ChordSubstitution(Base):
    """
    Chord substitution model - stores pre-computed chord substitution relationships.

    This table maps each source chord to its valid substitution options based on
    music theory principles (tritone, diatonic, chromatic, circle of fifths, etc.)
    """

    __tablename__ = "chord_substitutions"

    id = Column(Integer, primary_key=True, index=True)

    # Source chord (the original chord being substituted)
    source_chord_id = Column(Integer, ForeignKey("chords.id"), nullable=False, index=True)

    # Target chord (the substitution option)
    target_chord_id = Column(Integer, ForeignKey("chords.id"), nullable=False, index=True)

    # Substitution technique
    technique = Column(String(50), nullable=False, index=True)
    # Examples: "tritone", "diatonic", "chromatic", "circle_fifths", "relative", "parallel"

    # Score indicating quality/strength of substitution (0.0-1.0)
    score = Column(Float, default=0.8, nullable=False)

    # Description of why this substitution works
    description = Column(Text, nullable=True)

    # Common usage context
    usage_context = Column(String(100), nullable=True)
    # Examples: "jazz", "classical", "pop", "blues", "ii-V-I", "turnaround"

    # Theoretical relationship
    relationship_type = Column(String(50), nullable=True)
    # Examples: "shared_tones", "voice_leading", "functional_substitute"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ChordSubstitution {self.source_chord_id} -> {self.target_chord_id} ({self.technique})>"
