from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.chord import Chord
from app.schemas.chord import ChordResponse, ChordWithExtensions

router = APIRouter()


@router.get("/", response_model=List[ChordResponse])
def list_chords(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all chords."""
    chords = db.query(Chord).offset(skip).limit(limit).all()
    return chords


@router.get("/{symbol}", response_model=ChordResponse)
def get_chord(symbol: str, db: Session = Depends(get_db)):
    """Get chord details by symbol."""
    chord = db.query(Chord).filter(Chord.symbol == symbol).first()
    if not chord:
        raise HTTPException(status_code=404, detail=f"Chord '{symbol}' not found")
    return chord


@router.get("/{symbol}/notes")
def get_chord_notes(symbol: str, db: Session = Depends(get_db)):
    """Get notes for a chord."""
    chord = db.query(Chord).filter(Chord.symbol == symbol).first()
    if not chord:
        raise HTTPException(status_code=404, detail=f"Chord '{symbol}' not found")

    return {
        "symbol": chord.symbol,
        "notes": chord.notes,
        "intervals": chord.intervals,
        "root_note": chord.root_note,
    }


@router.get("/{symbol}/extensions", response_model=ChordWithExtensions)
def get_chord_extensions(symbol: str, db: Session = Depends(get_db)):
    """Get possible extensions for a chord."""
    chord = db.query(Chord).filter(Chord.symbol == symbol).first()
    if not chord:
        raise HTTPException(status_code=404, detail=f"Chord '{symbol}' not found")

    # TODO: Implement extension calculation logic
    return ChordWithExtensions(
        symbol=chord.symbol,
        root_note=chord.root_note,
        notes=chord.notes,
        intervals=chord.intervals,
        chord_quality=chord.chord_quality,
        extensions=[],  # Will be implemented later
        tensions=[],
    )
