from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class KeySignatureBase(BaseModel):
    """Base key signature schema."""

    key_name: str = Field(..., description="e.g., 'C major', 'A minor'")
    tonic: str = Field(..., description="Tonic note")
    mode: str = Field(..., description="'major' or 'minor'")


class KeySignatureSchema(KeySignatureBase):
    """Complete key signature schema."""

    sharps_flats: int = Field(..., description="Number of sharps (+) or flats (-)")
    accidentals: List[str] = Field(..., description="List of sharps/flats")
    scale_notes: List[str] = Field(..., description="Notes in the scale")


class KeySignatureResponse(KeySignatureSchema):
    """Key signature response with database fields."""

    id: int
    diatonic_chords: List[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True
