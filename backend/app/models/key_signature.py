from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from sqlalchemy.sql import func
from app.database import Base


class KeySignature(Base):
    """Key signature model - stores key signature information."""

    __tablename__ = "key_signatures"

    id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String(10), unique=True, nullable=False)
    tonic = Column(String(5), nullable=False)
    mode = Column(String(20), nullable=False)
    sharps_flats = Column(Integer, nullable=False)
    accidentals = Column(ARRAY(String(5)), nullable=False)
    scale_notes = Column(ARRAY(String(5)), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<KeySignature {self.key_name}>"
