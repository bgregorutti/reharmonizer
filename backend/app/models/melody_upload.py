"""
Melody upload model - Store uploaded melody files and analysis results.
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Text
from sqlalchemy.sql import func
from app.database import Base


class MelodyUpload(Base):
    """
    Store uploaded melody files (MusicXML, MSCZ).
    """

    __tablename__ = "melody_uploads"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)  # 'musicxml' or 'mscz'
    file_path = Column(String(512), nullable=False)

    # Analysis results
    detected_key = Column(String(20))
    time_signature = Column(String(10))
    tempo = Column(Integer)
    measures = Column(Integer)
    duration = Column(Float)

    # Melody notes as JSON
    melody_notes = Column(JSON)

    # Metadata
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MelodyUpload(id={self.id}, file_name='{self.file_name}', key='{self.detected_key}')>"


class HarmonizationResult(Base):
    """
    Store harmonization results for uploaded melodies.
    """

    __tablename__ = "harmonization_results"

    id = Column(Integer, primary_key=True, index=True)
    melody_upload_id = Column(Integer, nullable=False)  # FK to melody_uploads

    style = Column(String(20), nullable=False)  # 'jazz', 'pop', 'classical'
    chord_progression = Column(JSON, nullable=False)  # List of chord symbols

    # Analysis metadata
    pattern_applied = Column(String(100))  # e.g., "ii-V-I"
    score = Column(Float)  # Quality score
    options = Column(JSON)  # Harmonization options used

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<HarmonizationResult(id={self.id}, style='{self.style}', melody_id={self.melody_upload_id})>"
