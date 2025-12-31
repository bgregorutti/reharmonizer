"""
API endpoints for melody upload and harmonization.
"""

import os
import tempfile
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.melody_upload import MelodyUpload, HarmonizationResult
from app.schemas.melody import (
    MelodyUploadResponse,
    MelodyAnalysis,
    MelodyNote,
    HarmonizationRequest,
    HarmonizationResponse,
    ChordRecommendation,
    ChordTiming,
)
from app.services.melody_harmonization import (
    MelodyParser,
    MelodyAnalyzer,
    ChordMatcher,
    StylePatterns,
    EnhancedHarmonizationEngine,
)

router = APIRouter()

# Allowed file extensions
ALLOWED_EXTENSIONS = {".xml", ".musicxml", ".mscz"}


@router.post("/upload", response_model=MelodyUploadResponse)
async def upload_melody(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    """
    Upload and analyze a melody file (MusicXML or MSCZ).

    Args:
        file: Uploaded file
        db: Database session

    Returns:
        Upload response with melody analysis
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Create temporary file to save upload
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "/tmp/melody_uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # Save file temporarily
        temp_path = os.path.join(upload_dir, f"temp_{file.filename}")
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Parse the melody
        parser = MelodyParser()
        parsed_data = parser.parse_file(temp_path)

        # Determine file type
        file_type = "musicxml" if file_ext in {".xml", ".musicxml"} else "mscz"

        # Create database record
        melody_upload = MelodyUpload(
            file_name=file.filename,
            file_type=file_type,
            file_path=temp_path,
            detected_key=parsed_data.get("key_signature"),
            time_signature=parsed_data.get("time_signature"),
            tempo=parsed_data.get("tempo"),
            measures=parsed_data.get("measures", 0),
            duration=parsed_data.get("duration", 0.0),
            melody_notes=parsed_data.get("notes", []),
        )

        db.add(melody_upload)
        db.commit()
        db.refresh(melody_upload)

        # Convert notes to Pydantic models
        melody_notes = [MelodyNote(**note) for note in parsed_data.get("notes", [])]

        # Create response
        analysis = MelodyAnalysis(
            notes=melody_notes,
            detected_key=parsed_data.get("key_signature"),
            time_signature=parsed_data.get("time_signature"),
            tempo=parsed_data.get("tempo"),
            measures=parsed_data.get("measures", 0),
            duration=parsed_data.get("duration", 0.0),
            parts=parsed_data.get("parts", 1),
        )

        return MelodyUploadResponse(
            id=melody_upload.id,
            file_name=file.filename,
            file_type=file_type,
            analysis=analysis,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@router.post("/harmonize", response_model=HarmonizationResponse)
def harmonize_melody(request: HarmonizationRequest, db: Session = Depends(get_db)):
    """
    Generate chord progression for an uploaded melody using pattern-based harmonization.

    Args:
        request: Harmonization request with melody ID and style
        db: Database session

    Returns:
        Harmonization result with chord progression and alternatives
    """
    # Get melody upload from database
    melody_upload = (
        db.query(MelodyUpload).filter_by(id=request.melody_upload_id).first()
    )

    if not melody_upload:
        raise HTTPException(status_code=404, detail="Melody upload not found")

    # Get melody notes
    melody_notes = melody_upload.melody_notes
    if not melody_notes:
        raise HTTPException(status_code=400, detail="No melody notes found")

    # Use enhanced harmonization engine
    engine = EnhancedHarmonizationEngine(db)

    # Generate harmonizations (primary + alternatives)
    harmonizations = engine.harmonize(
        melody_notes=melody_notes,
        key_signature=melody_upload.detected_key or "C major",
        style=request.style,
        num_alternatives=3,
    )

    if not harmonizations:
        raise HTTPException(
            status_code=400,
            detail="Could not generate chord progression for this melody",
        )

    # Use first harmonization as primary
    primary_harmonization = harmonizations[0]

    # Convert chord details to Pydantic models
    chord_details_list = []
    for chord_detail in primary_harmonization.get("chord_details", []):
        chord_details_list.append(
            ChordRecommendation(
                symbol=chord_detail.get("symbol", "C"),
                root_note=chord_detail.get("root_note", "C"),
                notes=chord_detail.get("notes", ["C", "E", "G"]),
                chord_quality=chord_detail.get("chord_quality", "major"),
                score=chord_detail.get("score", 0.5),
            )
        )

    # Convert chord timing to Pydantic models
    chord_timing_list = []
    for timing in primary_harmonization.get("chord_timing", []):
        chord_timing_list.append(
            ChordTiming(
                symbol=timing.get("symbol", "C"),
                measure=timing.get("measure", 1),
                offset=timing.get("offset", 0.0),
                duration=timing.get("duration", 4.0),
            )
        )

    # Generate alternatives list (just chord symbols) and their timing
    alternatives = []
    alternatives_timing = []
    for harm in harmonizations[1:]:
        alternatives.append(harm.get("chord_progression", []))

        # Convert timing for this alternative
        alt_timing = []
        for timing in harm.get("chord_timing", []):
            alt_timing.append(
                ChordTiming(
                    symbol=timing.get("symbol", "C"),
                    measure=timing.get("measure", 1),
                    offset=timing.get("offset", 0.0),
                    duration=timing.get("duration", 4.0),
                )
            )
        alternatives_timing.append(alt_timing)

    # Save harmonization result to database
    harmonization = HarmonizationResult(
        melody_upload_id=request.melody_upload_id,
        style=request.style,
        chord_progression=primary_harmonization.get("chord_progression", []),
        pattern_applied=primary_harmonization.get("pattern_name"),
        score=primary_harmonization.get("score", 0.5),
        options=request.options or {},
    )

    db.add(harmonization)
    db.commit()
    db.refresh(harmonization)

    # Return response
    return HarmonizationResponse(
        id=harmonization.id,
        melody_upload_id=request.melody_upload_id,
        style=request.style,
        chord_progression=primary_harmonization.get("chord_progression", []),
        chord_details=chord_details_list,
        chord_timing=chord_timing_list,
        pattern_applied=primary_harmonization.get("pattern_name"),
        score=primary_harmonization.get("score", 0.5),
        alternatives=alternatives if len(alternatives) > 0 else None,
        alternatives_timing=alternatives_timing if len(alternatives_timing) > 0 else None,
    )


@router.get("/uploads/{upload_id}", response_model=MelodyUploadResponse)
def get_melody_upload(upload_id: int, db: Session = Depends(get_db)):
    """
    Get a melody upload by ID.

    Args:
        upload_id: Melody upload ID
        db: Database session

    Returns:
        Melody upload with analysis
    """
    melody_upload = db.query(MelodyUpload).filter_by(id=upload_id).first()

    if not melody_upload:
        raise HTTPException(status_code=404, detail="Melody upload not found")

    # Convert notes to Pydantic models
    melody_notes = [MelodyNote(**note) for note in melody_upload.melody_notes or []]

    # Create response
    analysis = MelodyAnalysis(
        notes=melody_notes,
        detected_key=melody_upload.detected_key,
        time_signature=melody_upload.time_signature,
        tempo=melody_upload.tempo,
        measures=melody_upload.measures or 0,
        duration=melody_upload.duration or 0.0,
        parts=1,  # Stored in upload if needed
    )

    return MelodyUploadResponse(
        id=melody_upload.id,
        file_name=melody_upload.file_name,
        file_type=melody_upload.file_type,
        analysis=analysis,
    )
