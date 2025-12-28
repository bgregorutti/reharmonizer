from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.key_signature import KeySignature
from app.schemas.key_signature import KeySignatureResponse

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

    # TODO: Implement diatonic chord generation using music21
    return {"key": key_name, "chords": [], "message": "To be implemented with music21"}


@router.get("/{key_name}/scale")
def get_key_scale(key_name: str, db: Session = Depends(get_db)):
    """Get scale notes for a key."""
    key = db.query(KeySignature).filter(KeySignature.key_name == key_name).first()
    if not key:
        raise HTTPException(status_code=404, detail=f"Key '{key_name}' not found")

    return {"key": key_name, "scale_notes": key.scale_notes, "mode": key.mode}
