from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ChordBase(BaseModel):
    """Base chord schema."""

    symbol: str = Field(..., description="Chord symbol, e.g., 'Cmaj7'")
    root_note: str = Field(..., description="Root note, e.g., 'C'")


class ChordSchema(ChordBase):
    """Complete chord schema."""

    notes: List[str] = Field(..., description="Notes in the chord")
    intervals: List[int] = Field(..., description="Intervals from root in semitones")
    chord_quality: Optional[str] = Field(None, description="Quality: major7, minor7, etc.")


class ChordWithExtensions(ChordSchema):
    """Chord schema with extensions and tensions."""

    extensions: List[str] = Field(default_factory=list, description="Available extensions")
    tensions: List[str] = Field(default_factory=list, description="Available tensions")
    avoid_notes: Optional[List[str]] = Field(default_factory=list, description="Avoid notes")


class ChordResponse(ChordSchema):
    """Chord response schema with database fields."""

    id: int
    roman_numeral: Optional[str] = None
    function: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
