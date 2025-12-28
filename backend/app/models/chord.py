from sqlalchemy import Column, Integer, String, ARRAY, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Chord(Base):
    """Chord model - stores chord definitions and properties."""

    __tablename__ = "chords"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)
    root_note = Column(String(5), nullable=False)
    chord_quality = Column(String(20), nullable=False)
    intervals = Column(ARRAY(Integer), nullable=False)
    notes = Column(ARRAY(String(5)), nullable=False)
    roman_numeral = Column(String(10), nullable=True)
    function = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Chord {self.symbol}>"
