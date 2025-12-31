from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import any_
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


@router.get("/search/by-note", response_model=List[ChordResponse])
def search_chords_by_note(
    note: str,
    scale_type: str = "major",
    db: Session = Depends(get_db)
):
    """
    Search for all chords that contain a specific note.

    Args:
        note: The note to search for (e.g., "C", "D#", "Eb")
        scale_type: The scale type for context (major or minor) - currently for reference

    Returns:
        List of chords containing the specified note
    """
    # Normalize the note to handle enharmonic equivalents
    def normalize_note(note_name: str) -> str:
        """Normalize note name by removing octave and converting accidentals."""
        note_name = note_name.replace("♭", "-").replace("♯", "#")
        base_note = note_name.rstrip("0123456789")
        return base_note

    # Create enharmonic equivalents map
    enharmonic_map = {
        "C#": ["C#", "D-"],
        "D-": ["C#", "D-"],
        "D#": ["D#", "E-"],
        "E-": ["D#", "E-"],
        "F#": ["F#", "G-"],
        "G-": ["F#", "G-"],
        "G#": ["G#", "A-"],
        "A-": ["G#", "A-"],
        "A#": ["A#", "B-"],
        "B-": ["A#", "B-"],
        "C-": ["B", "C-"],
        "E#": ["E#", "F"],
        "B#": ["B#", "C"],
        "F-": ["E", "F-"],
    }

    normalized_note = normalize_note(note)

    # Get enharmonic equivalents
    search_notes = enharmonic_map.get(normalized_note, [normalized_note])

    # Search for chords containing any of the enharmonic equivalents
    chords = []
    for search_note in search_notes:
        # Query chords where the notes array contains the search note
        # Use any_() to check if the note is in the array
        matching_chords = db.query(Chord).filter(
            search_note == any_(Chord.notes)
        ).all()
        chords.extend(matching_chords)

    # Remove duplicates while preserving order
    seen = set()
    unique_chords = []
    for chord in chords:
        if chord.id not in seen:
            seen.add(chord.id)
            unique_chords.append(chord)

    if not unique_chords:
        raise HTTPException(
            status_code=404,
            detail=f"No chords found containing note '{note}'"
        )

    return unique_chords
