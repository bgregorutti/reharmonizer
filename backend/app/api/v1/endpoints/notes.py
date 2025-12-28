"""Notes and improvisation endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.reharmonization.engine import ReharmonizationEngine

router = APIRouter()


@router.get("/improvisation/notes/{chord_symbol}")
def get_improvisation_notes(chord_symbol: str, count: int = 5, db: Session = Depends(get_db)):
    """
    Get improvisation notes for a chord.

    Returns chord tones, scale notes, and recommended notes for improvisation.
    """
    engine = ReharmonizationEngine(db)

    # Get note recommendations
    result = engine.recommend_improvisation_notes(chord_symbol, count)

    return result
