"""
Generate chord substitutions based on music theory principles.

This script creates all possible chord substitution relationships and stores them
in the database. It implements various substitution techniques:
- Tritone substitution
- Diatonic substitution
- Chromatic substitution
- Circle of fifths
- Relative/parallel chord substitutions
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Chord, ChordSubstitution
from music21 import pitch, interval


class SubstitutionGenerator:
    """Generates chord substitution relationships based on music theory."""

    # Note mapping for calculations
    NOTE_TO_SEMITONE = {
        "C": 0, "C#": 1, "D-": 1, "D": 2, "D#": 3, "E-": 3,
        "E": 4, "F": 5, "F#": 6, "G-": 6, "G": 7, "G#": 8,
        "A-": 8, "A": 9, "A#": 10, "B-": 10, "B": 11, "C-": 11
    }

    SEMITONE_TO_NOTE = {
        0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F",
        6: "F#", 7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B"
    }

    def __init__(self, db):
        """Initialize the substitution generator."""
        self.db = db
        self.chords = {}  # symbol -> chord object mapping
        self.load_chords()

    def load_chords(self):
        """Load all chords from database."""
        chords = self.db.query(Chord).all()
        for chord in chords:
            self.chords[chord.symbol] = chord
        print(f"Loaded {len(self.chords)} chords from database")

    def normalize_note(self, note_name):
        """Normalize note name to handle enharmonic equivalents."""
        # Remove octave numbers
        note_name = note_name.replace("♭", "-").replace("♯", "#")
        base_note = note_name.rstrip("0123456789")
        return base_note

    def get_semitone(self, note_name):
        """Get semitone number for a note."""
        normalized = self.normalize_note(note_name)
        return self.NOTE_TO_SEMITONE.get(normalized, 0)

    def transpose_note(self, note_name, semitones):
        """Transpose a note by a given number of semitones."""
        base_semitone = self.get_semitone(note_name)
        new_semitone = (base_semitone + semitones) % 12
        return self.SEMITONE_TO_NOTE[new_semitone]

    def count_common_notes(self, chord1, chord2):
        """Count common notes between two chords."""
        notes1 = set(self.normalize_note(n) for n in chord1.notes)
        notes2 = set(self.normalize_note(n) for n in chord2.notes)
        return len(notes1 & notes2)

    def generate_tritone_substitution(self, source_chord):
        """
        Generate tritone substitution.

        Tritone substitution: Replace a dominant 7th chord with another dominant 7th
        chord whose root is a tritone (6 semitones) away.

        Example: C7 -> F#7 (Gb7)
        """
        substitutions = []

        # Only works for dominant 7th chords
        if source_chord.chord_quality != "dominant7":
            return substitutions

        # Find target semitone (tritone away - 6 semitones)
        source_semitone = self.get_semitone(source_chord.root_note)
        target_semitone = (source_semitone + 6) % 12

        # Find matching dominant 7th chords with enharmonic equivalence
        for symbol, chord in self.chords.items():
            if (chord.chord_quality == "dominant7" and
                self.get_semitone(chord.root_note) == target_semitone and
                chord.id != source_chord.id):

                substitutions.append({
                    "target_chord": chord,
                    "technique": "tritone",
                    "score": 0.95,
                    "description": f"Tritone substitution: {source_chord.symbol} and {chord.symbol} share the same tritone (3rd and 7th)",
                    "usage_context": "jazz",
                    "relationship_type": "shared_tones"
                })

        return substitutions

    def generate_diatonic_substitution(self, source_chord):
        """
        Generate diatonic substitutions.

        Diatonic substitution: Chords that share many common tones within the same key.

        Common diatonic substitutions:
        - I ↔ iii (share 2 notes)
        - I ↔ vi (relative minor)
        - ii ↔ IV (share 2 notes)
        - V ↔ vii° (share 2 notes)
        """
        substitutions = []

        for symbol, chord in self.chords.items():
            if chord.id == source_chord.id:
                continue

            # Count common notes
            common_notes = self.count_common_notes(source_chord, chord)

            # If they share 2+ notes, it's a good diatonic substitution
            if common_notes >= 2:
                score = min(0.9, 0.5 + (common_notes * 0.2))

                substitutions.append({
                    "target_chord": chord,
                    "technique": "diatonic",
                    "score": score,
                    "description": f"Shares {common_notes} common tone(s) with {source_chord.symbol}",
                    "usage_context": "classical",
                    "relationship_type": "shared_tones"
                })

        return substitutions

    def generate_relative_substitution(self, source_chord):
        """
        Generate relative major/minor substitutions.

        Relative substitution: Major chord ↔ its relative minor (3 semitones down)
        Example: C major ↔ A minor
        """
        substitutions = []

        if source_chord.chord_quality == "major":
            # Find relative minor (3 semitones down)
            source_semitone = self.get_semitone(source_chord.root_note)
            target_semitone = (source_semitone - 3) % 12
            target_quality = "minor"

        elif source_chord.chord_quality == "minor":
            # Find relative major (3 semitones up)
            source_semitone = self.get_semitone(source_chord.root_note)
            target_semitone = (source_semitone + 3) % 12
            target_quality = "major"
        else:
            return substitutions

        # Find matching chords with enharmonic equivalence
        for symbol, chord in self.chords.items():
            if (self.get_semitone(chord.root_note) == target_semitone and
                chord.chord_quality == target_quality and
                chord.id != source_chord.id):

                substitutions.append({
                    "target_chord": chord,
                    "technique": "relative",
                    "score": 0.90,
                    "description": f"Relative major/minor: {source_chord.symbol} and {chord.symbol} share the same key signature",
                    "usage_context": "classical",
                    "relationship_type": "functional_substitute"
                })

        return substitutions

    def generate_parallel_substitution(self, source_chord):
        """
        Generate parallel major/minor substitutions.

        Parallel substitution: Same root note, different quality
        Example: C major ↔ C minor
        """
        substitutions = []

        if source_chord.chord_quality == "major":
            target_qualities = ["minor", "minor7"]
        elif source_chord.chord_quality == "minor":
            target_qualities = ["major", "major7"]
        else:
            return substitutions

        # Find chords with same root but different quality (with enharmonic equivalence)
        source_semitone = self.get_semitone(source_chord.root_note)

        for symbol, chord in self.chords.items():
            if (self.get_semitone(chord.root_note) == source_semitone and
                chord.chord_quality in target_qualities and
                chord.id != source_chord.id):

                substitutions.append({
                    "target_chord": chord,
                    "technique": "parallel",
                    "score": 0.75,
                    "description": f"Parallel major/minor: Same root note as {source_chord.symbol}, different quality",
                    "usage_context": "pop",
                    "relationship_type": "functional_substitute"
                })

        return substitutions

    def generate_circle_fifths_substitution(self, source_chord):
        """
        Generate circle of fifths substitutions.

        Circle of fifths: Chords related by fifth intervals (up or down)
        Example: C -> G (up 5th), C -> F (down 5th / up 4th)
        """
        substitutions = []

        # Calculate target semitones with enharmonic equivalence
        source_semitone = self.get_semitone(source_chord.root_note)
        # Up a fifth (7 semitones)
        target_up_fifth_semitone = (source_semitone + 7) % 12
        # Down a fifth (5 semitones) = up a fourth
        target_down_fifth_semitone = (source_semitone + 5) % 12

        for symbol, chord in self.chords.items():
            if chord.id == source_chord.id:
                continue

            chord_semitone = self.get_semitone(chord.root_note)

            if chord_semitone in [target_up_fifth_semitone, target_down_fifth_semitone]:
                # Prefer same quality
                if chord.chord_quality == source_chord.chord_quality:
                    score = 0.85
                else:
                    score = 0.70

                direction = "fifth up" if chord_semitone == target_up_fifth_semitone else "fourth up"

                substitutions.append({
                    "target_chord": chord,
                    "technique": "circle_fifths",
                    "score": score,
                    "description": f"Circle of fifths: {chord.symbol} is a {direction} from {source_chord.symbol}",
                    "usage_context": "jazz",
                    "relationship_type": "voice_leading"
                })

        return substitutions

    def generate_chromatic_substitution(self, source_chord):
        """
        Generate chromatic approach chord substitutions.

        Chromatic substitution: Chords a semitone above or below the source chord
        Example: C7 -> C#7 -> D7 (chromatic approach)
        """
        substitutions = []

        # Calculate target semitones with enharmonic equivalence
        source_semitone = self.get_semitone(source_chord.root_note)
        # Half step up
        target_up_semitone = (source_semitone + 1) % 12
        # Half step down
        target_down_semitone = (source_semitone - 1) % 12

        for symbol, chord in self.chords.items():
            if chord.id == source_chord.id:
                continue

            chord_semitone = self.get_semitone(chord.root_note)

            if chord_semitone in [target_up_semitone, target_down_semitone]:
                # Prefer dominant 7th for chromatic approaches
                if chord.chord_quality == "dominant7":
                    score = 0.80
                elif chord.chord_quality == source_chord.chord_quality:
                    score = 0.70
                else:
                    score = 0.60

                direction = "semitone up" if chord_semitone == target_up_semitone else "semitone down"

                substitutions.append({
                    "target_chord": chord,
                    "technique": "chromatic",
                    "score": score,
                    "description": f"Chromatic approach: {chord.symbol} is a {direction} from {source_chord.symbol}",
                    "usage_context": "jazz",
                    "relationship_type": "voice_leading"
                })

        return substitutions

    def generate_all_substitutions(self):
        """Generate all chord substitution relationships."""
        print("\nGenerating chord substitutions...")

        all_substitutions = []
        technique_counts = {}

        for symbol, source_chord in self.chords.items():
            print(f"  Processing {symbol}...")

            # Generate all types of substitutions
            techniques = [
                self.generate_tritone_substitution,
                self.generate_diatonic_substitution,
                self.generate_relative_substitution,
                self.generate_parallel_substitution,
                self.generate_circle_fifths_substitution,
                self.generate_chromatic_substitution,
            ]

            for technique_func in techniques:
                substitutions = technique_func(source_chord)

                for sub in substitutions:
                    # Create ChordSubstitution object
                    chord_sub = ChordSubstitution(
                        source_chord_id=source_chord.id,
                        target_chord_id=sub["target_chord"].id,
                        technique=sub["technique"],
                        score=sub["score"],
                        description=sub["description"],
                        usage_context=sub["usage_context"],
                        relationship_type=sub["relationship_type"],
                    )

                    all_substitutions.append(chord_sub)

                    # Track counts
                    technique = sub["technique"]
                    technique_counts[technique] = technique_counts.get(technique, 0) + 1

        # Bulk insert
        if all_substitutions:
            self.db.bulk_save_objects(all_substitutions)
            self.db.commit()

        print(f"\n✓ Generated {len(all_substitutions)} chord substitution relationships")
        print("\nBreakdown by technique:")
        for technique, count in sorted(technique_counts.items()):
            print(f"  {technique}: {count}")

        return all_substitutions


def main():
    """Main function to generate substitutions."""
    print("=" * 60)
    print("Chord Substitution Generator")
    print("=" * 60)

    db = SessionLocal()

    try:
        # Check if we have chords in the database
        chord_count = db.query(Chord).count()
        if chord_count == 0:
            print("\n⚠ No chords found in database!")
            print("Please run 'python scripts/seed_database.py' first.")
            return

        print(f"\nFound {chord_count} chords in database")

        # Clear existing substitutions
        existing_count = db.query(ChordSubstitution).count()
        if existing_count > 0:
            print(f"Clearing {existing_count} existing substitutions...")
            db.query(ChordSubstitution).delete()
            db.commit()

        # Generate new substitutions
        generator = SubstitutionGenerator(db)
        generator.generate_all_substitutions()

        print("\n" + "=" * 60)
        print("✓ Chord substitution generation completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
