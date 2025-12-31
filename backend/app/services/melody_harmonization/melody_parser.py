"""
Melody parser - Parse MusicXML and MSCZ files using music21.
"""

from typing import List, Dict, Any, Optional
import music21
from music21 import stream, note, chord as m21_chord, meter, key


class MelodyParser:
    """
    Parse MusicXML and MSCZ files to extract melody information.
    """

    def __init__(self):
        """Initialize the melody parser."""
        pass

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a MusicXML or MSCZ file and extract melody information.

        Args:
            file_path: Path to the MusicXML or MSCZ file

        Returns:
            Dictionary containing melody data:
            {
                "notes": List of note dictionaries,
                "key_signature": Detected key signature,
                "time_signature": Time signature,
                "tempo": Tempo (if available),
                "measures": Number of measures,
                "parts": Number of parts/voices
            }
        """
        try:
            # Parse the file using music21
            score = music21.converter.parse(file_path)

            # Extract metadata
            metadata = self._extract_metadata(score)

            # Extract melody (assume top part is melody)
            melody_notes = self._extract_melody(score)

            return {
                "notes": melody_notes,
                "key_signature": metadata["key_signature"],
                "time_signature": metadata["time_signature"],
                "tempo": metadata["tempo"],
                "measures": metadata["measures"],
                "parts": metadata["parts"],
                "duration": metadata["duration"],
            }

        except Exception as e:
            raise ValueError(f"Failed to parse music file: {str(e)}")

    def _extract_metadata(self, score: stream.Score) -> Dict[str, Any]:
        """
        Extract metadata from the score.

        Args:
            score: music21 Score object

        Returns:
            Dictionary with metadata
        """
        metadata = {
            "key_signature": None,
            "time_signature": None,
            "tempo": None,
            "measures": 0,
            "parts": len(score.parts),
            "duration": 0.0,
        }

        # Get first part for analysis
        if score.parts:
            first_part = score.parts[0]

            # Extract key signature
            key_obj = first_part.analyze("key")
            if key_obj:
                metadata["key_signature"] = f"{key_obj.tonic.name} {key_obj.mode}"

            # Extract time signature
            time_sigs = first_part.flatten().getElementsByClass(meter.TimeSignature)
            if time_sigs:
                ts = time_sigs[0]
                metadata["time_signature"] = f"{ts.numerator}/{ts.denominator}"

            # Extract tempo
            tempos = first_part.flatten().getElementsByClass(music21.tempo.MetronomeMark)
            if tempos:
                metadata["tempo"] = int(tempos[0].number)

            # Count measures
            metadata["measures"] = len(first_part.getElementsByClass(stream.Measure))

            # Get duration
            metadata["duration"] = float(first_part.duration.quarterLength)

        return metadata

    def _extract_melody(self, score: stream.Score) -> List[Dict[str, Any]]:
        """
        Extract melody notes from the score.
        Assumes the melody is in the top part (first part).

        Args:
            score: music21 Score object

        Returns:
            List of note dictionaries with pitch, duration, offset, etc.
        """
        melody_notes = []

        if not score.parts:
            return melody_notes

        # Get the top part (usually melody)
        melody_part = score.parts[0]

        # Flatten to get all notes in order
        flat_part = melody_part.flatten()

        # Extract notes and chords
        for element in flat_part.notesAndRests:
            if isinstance(element, note.Note):
                # Single note
                melody_notes.append(
                    {
                        "type": "note",
                        "pitch": element.pitch.nameWithOctave,
                        "pitch_class": element.pitch.name,
                        "midi": element.pitch.midi,
                        "duration": float(element.duration.quarterLength),
                        "offset": float(element.offset),
                        "measure": element.measureNumber,
                        "is_rest": False,
                    }
                )
            elif isinstance(element, m21_chord.Chord):
                # Chord - extract highest note as melody
                highest_note = element.pitches[-1]  # Pitches are sorted low to high
                melody_notes.append(
                    {
                        "type": "chord",
                        "pitch": highest_note.nameWithOctave,
                        "pitch_class": highest_note.name,
                        "midi": highest_note.midi,
                        "duration": float(element.duration.quarterLength),
                        "offset": float(element.offset),
                        "measure": element.measureNumber,
                        "is_rest": False,
                        "chord_notes": [p.nameWithOctave for p in element.pitches],
                    }
                )
            elif isinstance(element, note.Rest):
                # Rest
                melody_notes.append(
                    {
                        "type": "rest",
                        "pitch": None,
                        "pitch_class": None,
                        "midi": None,
                        "duration": float(element.duration.quarterLength),
                        "offset": float(element.offset),
                        "measure": element.measureNumber,
                        "is_rest": True,
                    }
                )

        return melody_notes

    def get_important_notes(
        self, melody_notes: List[Dict[str, Any]], threshold_duration: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Filter melody notes to get the most important ones.
        Important notes are:
        - Long notes (duration >= threshold)
        - Downbeat notes (offset % 4 == 0 in 4/4 time)

        Args:
            melody_notes: List of note dictionaries
            threshold_duration: Minimum duration for a note to be considered important

        Returns:
            List of important note dictionaries
        """
        important = []

        for note_dict in melody_notes:
            if note_dict["is_rest"]:
                continue

            # Long notes
            if note_dict["duration"] >= threshold_duration:
                important.append(note_dict)
                continue

            # Downbeat notes (simplified - offset is multiple of 4 quarter notes)
            if note_dict["offset"] % 4 == 0:
                important.append(note_dict)
                continue

        return important
