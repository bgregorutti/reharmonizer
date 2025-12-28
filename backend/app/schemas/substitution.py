from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class SubstitutionContext(BaseModel):
    """Context for chord substitution."""

    key: Optional[str] = None
    previous_chord: Optional[str] = None
    next_chord: Optional[str] = None
    position: Optional[str] = None  # Roman numeral


class SubstitutionRequest(BaseModel):
    """Request for chord substitutions."""

    chord: str = Field(..., description="Original chord")
    context: Optional[SubstitutionContext] = None
    techniques: List[str] = Field(default=["all"], description="Techniques to use")


class SubstitutionOption(BaseModel):
    """A single substitution option."""

    chord: str
    technique: str
    description: str
    common_usage: Optional[str] = None
    score: float = Field(ge=0, le=1)


class SubstitutionResponse(BaseModel):
    """Response with substitution options."""

    original_chord: str
    substitutions: List[SubstitutionOption]


class ReharmonizationRequest(BaseModel):
    """Request for reharmonization."""

    key_signature: Optional[str] = None
    chords: List[str] = Field(..., min_length=1)
    options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ReharmonizationSuggestion(BaseModel):
    """A single reharmonization suggestion."""

    chords: List[str]
    technique: str
    score: float
    analysis: Dict[str, Any]


class ReharmonizationResponse(BaseModel):
    """Response with reharmonization suggestions."""

    original: List[str]
    suggestions: List[ReharmonizationSuggestion]
    analysis: Dict[str, Any]
