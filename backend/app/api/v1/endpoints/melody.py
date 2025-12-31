"""
API endpoints for melody upload and harmonization.
"""

import os
import tempfile
import shutil
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import music21 as m21

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


@router.get("/harmonization/{harmonization_id}/export/musicxml")
def export_musicxml(harmonization_id: int, db: Session = Depends(get_db)):
    """
    Export harmonization result as MusicXML file.

    Args:
        harmonization_id: Harmonization result ID
        db: Database session

    Returns:
        MusicXML file download
    """
    # Get harmonization result
    harmonization = (
        db.query(HarmonizationResult).filter_by(id=harmonization_id).first()
    )

    if not harmonization:
        raise HTTPException(status_code=404, detail="Harmonization not found")

    # Get melody upload
    melody_upload = (
        db.query(MelodyUpload).filter_by(id=harmonization.melody_upload_id).first()
    )

    if not melody_upload:
        raise HTTPException(status_code=404, detail="Melody upload not found")

    try:
        # Create music21 score
        score = m21.stream.Score()

        # Add metadata
        score.metadata = m21.metadata.Metadata()
        score.metadata.title = f"Harmonization - {melody_upload.file_name}"
        score.metadata.composer = "Reharmonizer AI"

        # Create parts
        melody_part = m21.stream.Part()
        melody_part.id = "Melody"

        # Add melody notes
        melody_notes = melody_upload.melody_notes or []
        for note_data in melody_notes:
            try:
                # Skip notes with zero or negative duration
                duration_ql = note_data.get("duration", 1.0)
                if duration_ql <= 0.0:
                    print(f"Skipping note with zero duration: {note_data}")
                    continue

                if note_data.get("is_rest"):
                    note_obj = m21.note.Rest()
                else:
                    pitch_str = note_data.get("pitch", "C4")
                    note_obj = m21.note.Note(pitch_str)

                # Set duration (in quarter notes)
                note_obj.quarterLength = duration_ql

                melody_part.append(note_obj)
            except Exception as e:
                print(f"Error adding note: {e}")
                continue

        # Add chord symbols
        chord_progression = harmonization.chord_progression or []
        for i, chord_symbol in enumerate(chord_progression):
            try:
                # Create harmony object (chord symbol)
                cs = m21.harmony.ChordSymbol(chord_symbol)

                # Calculate offset based on measure (simplified)
                # Each measure is 4 quarter notes in 4/4 time
                cs.offset = i * 4.0

                melody_part.insert(cs.offset, cs)
            except Exception as e:
                print(f"Error adding chord symbol {chord_symbol}: {e}")
                continue

        score.append(melody_part)

        # Export to MusicXML
        output_dir = "/tmp/reharmonizer_exports"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(
            output_dir, f"harmonization_{harmonization_id}.musicxml"
        )

        score.write("musicxml", fp=output_file)

        return FileResponse(
            path=output_file,
            media_type="application/vnd.recordare.musicxml+xml",
            filename=f"harmonization_{harmonization_id}.musicxml",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to export MusicXML: {str(e)}"
        )


@router.get("/harmonization/{harmonization_id}/export/pdf")
def export_pdf(harmonization_id: int, db: Session = Depends(get_db)):
    """
    Export harmonization result as PDF file.

    Args:
        harmonization_id: Harmonization result ID
        db: Database session

    Returns:
        PDF file download
    """
    # Get harmonization result
    harmonization = (
        db.query(HarmonizationResult).filter_by(id=harmonization_id).first()
    )

    if not harmonization:
        raise HTTPException(status_code=404, detail="Harmonization not found")

    # Get melody upload
    melody_upload = (
        db.query(MelodyUpload).filter_by(id=harmonization.melody_upload_id).first()
    )

    if not melody_upload:
        raise HTTPException(status_code=404, detail="Melody upload not found")

    try:
        # Create music21 score (same as MusicXML export)
        score = m21.stream.Score()

        # Add metadata
        score.metadata = m21.metadata.Metadata()
        score.metadata.title = f"Harmonization - {melody_upload.file_name}"
        score.metadata.composer = "Reharmonizer AI"

        # Create parts
        melody_part = m21.stream.Part()
        melody_part.id = "Melody"

        # Add melody notes
        melody_notes = melody_upload.melody_notes or []
        for note_data in melody_notes:
            try:
                # Skip notes with zero or negative duration
                duration_ql = note_data.get("duration", 1.0)
                if duration_ql <= 0.0:
                    print(f"Skipping note with zero duration: {note_data}")
                    continue

                if note_data.get("is_rest"):
                    note_obj = m21.note.Rest()
                else:
                    pitch_str = note_data.get("pitch", "C4")
                    note_obj = m21.note.Note(pitch_str)

                note_obj.quarterLength = duration_ql

                melody_part.append(note_obj)
            except Exception as e:
                print(f"Error adding note: {e}")
                continue

        # Add chord symbols using timing information
        chord_timing = harmonization.chord_timing if hasattr(harmonization, 'chord_timing') else []

        if chord_timing:
            # Use chord timing if available
            for timing in chord_timing:
                try:
                    cs = m21.harmony.ChordSymbol(timing.get('symbol', 'C'))
                    cs.offset = timing.get('offset', 0.0)
                    # Set duration explicitly to avoid zero-duration chords
                    duration_ql = timing.get('duration', 4.0)
                    if duration_ql > 0:
                        cs.quarterLength = duration_ql
                    else:
                        cs.quarterLength = 4.0  # Default to whole note
                    melody_part.insert(cs.offset, cs)
                except Exception as e:
                    print(f"Error adding chord symbol {timing.get('symbol')}: {e}")
                    continue
        else:
            # Fallback to simple progression
            chord_progression = harmonization.chord_progression or []
            for i, chord_symbol in enumerate(chord_progression):
                try:
                    cs = m21.harmony.ChordSymbol(chord_symbol)
                    cs.offset = i * 4.0
                    cs.quarterLength = 4.0  # Default to whole note
                    melody_part.insert(cs.offset, cs)
                except Exception as e:
                    print(f"Error adding chord symbol {chord_symbol}: {e}")
                    continue

        score.append(melody_part)

        # Add measures to help with formatting
        try:
            score.makeMeasures(inPlace=True)
        except Exception as e:
            print(f"Warning: Could not create measures: {e}")

        # Export to PDF using music21's LilyPond backend
        output_dir = "/tmp/reharmonizer_exports"
        os.makedirs(output_dir, exist_ok=True)
        # Note: music21 creates a .ly file first, then LilyPond creates the actual PDF
        # with .pdf.pdf extension
        base_file = os.path.join(output_dir, f"harmonization_{harmonization_id}.pdf")

        # Use music21's musicxml.m21ToXml and then external converter
        try:
            print(f"Attempting to write PDF for harmonization {harmonization_id}")
            print(f"Score duration: {score.duration.quarterLength}")
            score.write("lily.pdf", fp=base_file)

            # music21 creates the actual PDF with .pdf.pdf extension
            actual_pdf = base_file + ".pdf"

            # Check if the actual PDF was created
            if os.path.exists(actual_pdf):
                print(f"PDF written successfully to {actual_pdf}")
                output_file = actual_pdf
            else:
                # Fallback to base file (might be just the .ly file)
                print(f"Warning: {actual_pdf} not found, using {base_file}")
                output_file = base_file

        except Exception as err:
            print("ERROR writing PDF:", err)
            import traceback
            traceback.print_exc()
            # Fallback: create a simple PDF message if LilyPond not available
            raise HTTPException(
                status_code=501,
                detail=f"PDF export failed: {str(err)}",
            )

        return FileResponse(
            path=output_file,
            media_type="application/pdf",
            filename=f"harmonization_{harmonization_id}.pdf",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export PDF: {str(e)}")
