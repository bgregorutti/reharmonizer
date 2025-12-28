from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.substitution import (
    ReharmonizationRequest,
    ReharmonizationResponse,
    ReharmonizationSuggestion,
    SubstitutionRequest,
    SubstitutionResponse,
    SubstitutionOption,
)
from app.services.reharmonization.engine import ReharmonizationEngine

router = APIRouter()


@router.post("/", response_model=ReharmonizationResponse)
def reharmonize(request: ReharmonizationRequest, db: Session = Depends(get_db)):
    """
    Main reharmonization endpoint.

    Provides multiple reharmonization suggestions using various techniques.
    """
    engine = ReharmonizationEngine(db)

    # Get techniques from request options
    techniques = request.options.get("techniques", ["random"]) if request.options else ["random"]
    complexity = request.options.get("complexity", 3) if request.options else 3

    # Get reharmonization suggestions
    suggestions = engine.reharmonize_progression(
        chords=request.chords,
        key_signature=request.key_signature,
        techniques=techniques,
        complexity=complexity,
    )

    # Convert to response format
    suggestion_objects = [
        ReharmonizationSuggestion(
            chords=sug["chords"],
            technique=sug["technique"],
            score=sug["score"],
            analysis=sug["analysis"],
        )
        for sug in suggestions
    ]

    return ReharmonizationResponse(
        original=request.chords,
        suggestions=suggestion_objects,
        analysis={
            "key_signature": request.key_signature,
            "techniques_used": techniques,
            "complexity": complexity,
        },
    )


@router.get("/substitutions/{chord_symbol}", response_model=SubstitutionResponse)
def get_substitutions(
    chord_symbol: str, technique: str = "random", db: Session = Depends(get_db)
):
    """Get substitution options for a chord."""
    engine = ReharmonizationEngine(db)

    # Get chord substitutions
    substitutions = engine.recommend_chord_substitutions(
        source_chord=chord_symbol, technique=technique, count=5
    )

    # Convert to response format
    options = [
        SubstitutionOption(
            chord=sub["chord"],
            technique=sub["technique"],
            description=sub["description"],
            common_usage=f"Alternative to {chord_symbol}",
            score=sub["score"],
        )
        for sub in substitutions
    ]

    return SubstitutionResponse(original_chord=chord_symbol, substitutions=options)


@router.post("/substitutions/analyze", response_model=SubstitutionResponse)
def analyze_substitutions(request: SubstitutionRequest, db: Session = Depends(get_db)):
    """Analyze and suggest context-aware substitutions."""
    engine = ReharmonizationEngine(db)

    # Determine technique from request
    techniques = request.techniques if request.techniques else ["random"]
    technique = techniques[0] if "all" not in techniques else "random"

    # Get chord substitutions
    substitutions = engine.recommend_chord_substitutions(
        source_chord=request.chord, technique=technique, count=5
    )

    # Convert to response format
    options = [
        SubstitutionOption(
            chord=sub["chord"],
            technique=sub["technique"],
            description=sub["description"],
            common_usage=f"Alternative to {request.chord}",
            score=sub["score"],
        )
        for sub in substitutions
    ]

    return SubstitutionResponse(original_chord=request.chord, substitutions=options)
