"""
Pydantic schemas for melody harmonization endpoints.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MelodyNote(BaseModel):
    """Schema for a single melody note."""

    type: str = Field(..., description="Note type: 'note', 'chord', or 'rest'")
    pitch: Optional[str] = Field(None, description="Pitch with octave (e.g., 'C4')")
    pitch_class: Optional[str] = Field(None, description="Pitch class (e.g., 'C')")
    midi: Optional[int] = Field(None, description="MIDI note number")
    duration: float = Field(..., description="Duration in quarter notes")
    offset: float = Field(..., description="Offset from start in quarter notes")
    measure: Optional[int] = Field(None, description="Measure number")
    is_rest: bool = Field(..., description="Whether this is a rest")


class MelodyAnalysis(BaseModel):
    """Schema for melody analysis results."""

    notes: List[MelodyNote] = Field(..., description="List of melody notes")
    detected_key: Optional[str] = Field(None, description="Detected key signature")
    time_signature: Optional[str] = Field(None, description="Time signature")
    tempo: Optional[int] = Field(None, description="Tempo in BPM")
    measures: int = Field(..., description="Number of measures")
    duration: float = Field(..., description="Total duration in quarter notes")
    parts: int = Field(..., description="Number of parts in the score")


class MelodyUploadResponse(BaseModel):
    """Response after uploading a melody file."""

    id: int = Field(..., description="Upload ID")
    file_name: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File type (musicxml or mscz)")
    analysis: MelodyAnalysis = Field(..., description="Melody analysis results")


class ChordRecommendation(BaseModel):
    """Schema for a chord recommendation."""

    symbol: str = Field(..., description="Chord symbol (e.g., 'Cmaj7')")
    root_note: str = Field(..., description="Root note of the chord")
    notes: List[str] = Field(..., description="Notes in the chord")
    chord_quality: str = Field(..., description="Chord quality (major, minor, etc.)")
    score: float = Field(..., description="Confidence score (0.0 to 1.0)")


class ChordTiming(BaseModel):
    """Schema for chord timing information."""

    symbol: str = Field(..., description="Chord symbol (e.g., 'Cmaj7')")
    measure: int = Field(..., description="Starting measure number")
    offset: float = Field(..., description="Starting offset in quarter notes")
    duration: float = Field(..., description="Duration in quarter notes")


class HarmonizationRequest(BaseModel):
    """Request to harmonize a melody."""

    melody_upload_id: int = Field(..., description="ID of the uploaded melody")
    style: str = Field(
        "jazz", description="Harmonization style: jazz, pop, or classical"
    )
    options: Optional[Dict[str, Any]] = Field(
        None, description="Additional harmonization options"
    )


class HarmonizationResponse(BaseModel):
    """Response with harmonization results."""

    id: int = Field(..., description="Harmonization result ID")
    melody_upload_id: int = Field(..., description="ID of the melody")
    style: str = Field(..., description="Harmonization style used")
    chord_progression: List[str] = Field(
        ..., description="List of chord symbols in the progression"
    )
    chord_details: List[ChordRecommendation] = Field(
        ..., description="Detailed information for each chord"
    )
    chord_timing: List[ChordTiming] = Field(
        ..., description="Timing information for each chord"
    )
    pattern_applied: Optional[str] = Field(
        None, description="Name of the pattern applied (if any)"
    )
    score: float = Field(..., description="Overall quality score")
    alternatives: Optional[List[List[str]]] = Field(
        None, description="Alternative chord progressions"
    )
    alternatives_timing: Optional[List[List[ChordTiming]]] = Field(
        None, description="Timing information for alternative progressions"
    )


class HarmonizationListResponse(BaseModel):
    """Response with multiple harmonization options."""

    melody_upload_id: int = Field(..., description="ID of the melody")
    harmonizations: List[HarmonizationResponse] = Field(
        ..., description="List of harmonization results for different styles"
    )
