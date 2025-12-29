from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.key_signature import KeySignature
from app.schemas.key_signature import KeySignatureResponse
from app.schemas.chord import ChordSchema
from music21 import key as m21_key, roman, pitch as m21_pitch

router = APIRouter()


@router.get("/", response_model=List[KeySignatureResponse])
def list_keys(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all key signatures."""
    keys = db.query(KeySignature).offset(skip).limit(limit).all()
    response = []
    for key in keys:
        response.append(
            KeySignatureResponse(
                id=key.id,
                key_name=key.key_name,
                tonic=key.tonic,
                mode=key.mode,
                sharps_flats=key.sharps_flats,
                accidentals=key.accidentals,
                scale_notes=key.scale_notes,
                created_at=key.created_at,
                diatonic_chords=[],  # Will be calculated later
            )
        )
    return response


@router.get("/{key_name}", response_model=KeySignatureResponse)
def get_key(key_name: str, db: Session = Depends(get_db)):
    """Get key signature details."""
    key = db.query(KeySignature).filter(KeySignature.key_name == key_name).first()
    if not key:
        raise HTTPException(status_code=404, detail=f"Key '{key_name}' not found")

    return KeySignatureResponse(
        id=key.id,
        key_name=key.key_name,
        tonic=key.tonic,
        mode=key.mode,
        sharps_flats=key.sharps_flats,
        accidentals=key.accidentals,
        scale_notes=key.scale_notes,
        created_at=key.created_at,
        diatonic_chords=[],  # Will be calculated later
    )


@router.get("/{key_name}/chords")
def get_key_chords(key_name: str, db: Session = Depends(get_db)):
    """Get diatonic chords for a key."""
    key = db.query(KeySignature).filter(KeySignature.key_name == key_name).first()
    if not key:
        raise HTTPException(status_code=404, detail=f"Key '{key_name}' not found")

    # Generate diatonic chords using music21
    try:
        # Create music21 key object
        m21_key_obj = m21_key.Key(key.tonic, key.mode)

        # Define proper roman numeral patterns for major and minor keys
        if key.mode == "major":
            # Major key: I, ii, iii, IV, V, vi, vii°
            rn_patterns = ["I", "ii", "iii", "IV", "V", "vi", "viio"]
        else:
            # Natural minor key: i, ii°, III, iv, v, VI, VII
            rn_patterns = ["i", "iio", "III", "iv", "v", "VI", "VII"]

        diatonic_chords = []

        for rn_pattern in rn_patterns:
            # Get the roman numeral chord
            rn = roman.RomanNumeral(rn_pattern, m21_key_obj)

            # Determine chord quality
            if rn.isMajorTriad():
                quality = "major"
            elif rn.isMinorTriad():
                quality = "minor"
            elif rn.isDiminishedTriad():
                quality = "diminished"
            else:
                quality = "other"

            # Get chord symbol (e.g., "Dm", "G", "Bdim")
            root_note = rn.root().name
            if quality == "minor":
                symbol = f"{root_note}m"
            elif quality == "diminished":
                symbol = f"{root_note}dim"
            else:
                symbol = root_note

            # Get notes and intervals
            notes = [p.name for p in rn.pitches]
            root_midi = rn.root().midi
            intervals = [p.midi - root_midi for p in rn.pitches]

            # Create chord schema
            chord_data = ChordSchema(
                symbol=symbol,
                root_note=root_note,
                chord_quality=quality,
                notes=notes,
                intervals=intervals
            )

            diatonic_chords.append(chord_data)

        return {"key": key_name, "chords": diatonic_chords}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating diatonic chords: {str(e)}"
        )


@router.get("/{key_name}/scale")
def get_key_scale(key_name: str, db: Session = Depends(get_db)):
    """Get scale notes for a key."""
    key = db.query(KeySignature).filter(KeySignature.key_name == key_name).first()
    if not key:
        raise HTTPException(status_code=404, detail=f"Key '{key_name}' not found")

    return {"key": key_name, "scale_notes": key.scale_notes, "mode": key.mode}
