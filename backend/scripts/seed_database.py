"""
Database seeding script.

Seeds the database with:
- Common chords (major, minor, dominant, etc.)
- All major and minor key signatures
- Basic substitution rules
- Common reharmonization patterns
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import Chord, KeySignature, SubstitutionRule, ReharmonizationPattern
from music21 import chord as m21_chord, key as m21_key


def seed_chords(db):
    """Seed common chords."""
    print("Seeding chords...")

    common_chords = [
        # Major chords
        "C", "D", "E", "F", "G", "A", "B",
        # Minor chords
        "Cm", "Dm", "Em", "Fm", "Gm", "Am", "Bm",
        # Major 7th chords
        "Cmaj7", "Dmaj7", "Emaj7", "Fmaj7", "Gmaj7", "Amaj7", "Bmaj7",
        # Minor 7th chords
        "Cm7", "Dm7", "Em7", "Fm7", "Gm7", "Am7", "Bm7",
        # Dominant 7th chords
        "C7", "D7", "E7", "F7", "G7", "A7", "B7",
    ]

    for chord_symbol in common_chords:
        try:
            # Use music21 to parse chord
            m21_c = m21_chord.Chord(chord_symbol)

            # Determine chord quality
            if m21_c.isMajorTriad():
                quality = "major"
            elif m21_c.isMinorTriad():
                quality = "minor"
            elif m21_c.isDominantSeventh():
                quality = "dominant7"
            elif m21_c.isMajorSeventh():
                quality = "major7"
            elif m21_c.isMinorSeventh():
                quality = "minor7"
            else:
                quality = "other"

            chord_obj = Chord(
                symbol=chord_symbol,
                root_note=m21_c.root().name,
                chord_quality=quality,
                intervals=[p.midi - m21_c.root().midi for p in m21_c.pitches],
                notes=[p.name for p in m21_c.pitches],
            )

            db.add(chord_obj)
            print(f"  Added chord: {chord_symbol}")

        except Exception as e:
            print(f"  Error adding chord {chord_symbol}: {e}")
            continue

    db.commit()
    print(f"Seeded {len(common_chords)} chords")


def seed_key_signatures(db):
    """Seed all major and minor key signatures."""
    print("Seeding key signatures...")

    # Major keys
    major_keys = ["C", "G", "D", "A", "E", "B", "F#", "Db", "Ab", "Eb", "Bb", "F"]
    # Relative minor keys
    minor_keys = ["A", "E", "B", "F#", "C#", "G#", "D#", "Bb", "F", "C", "G", "D"]

    count = 0

    # Seed major keys
    for key_name in major_keys:
        try:
            key_obj = m21_key.Key(key_name)
            sharps = key_obj.sharps

            key_sig = KeySignature(
                key_name=f"{key_name} major",
                tonic=key_name,
                mode="major",
                sharps_flats=sharps,
                accidentals=[],  # Can be computed from sharps/flats
                scale_notes=[p.name for p in key_obj.pitches],
            )

            db.add(key_sig)
            count += 1
            print(f"  Added key: {key_name} major")

        except Exception as e:
            print(f"  Error adding key {key_name} major: {e}")

    # Seed minor keys
    for key_name in minor_keys:
        try:
            key_obj = m21_key.Key(key_name, "minor")
            sharps = key_obj.sharps

            key_sig = KeySignature(
                key_name=f"{key_name} minor",
                tonic=key_name,
                mode="minor",
                sharps_flats=sharps,
                accidentals=[],  # Can be computed from sharps/flats
                scale_notes=[p.name for p in key_obj.pitches],
            )

            db.add(key_sig)
            count += 1
            print(f"  Added key: {key_name} minor")

        except Exception as e:
            print(f"  Error adding key {key_name} minor: {e}")

    db.commit()
    print(f"Seeded {count} key signatures")


def seed_substitution_rules(db):
    """Seed basic substitution rules."""
    print("Seeding substitution rules...")

    rules = [
        {
            "rule_name": "Tritone Substitution",
            "rule_type": "tritone",
            "source_chord_pattern": "V7",
            "target_chord_pattern": "bII7",
            "description": "Replace dominant 7th chord with chord a tritone away",
            "priority": 1,
        },
        {
            "rule_name": "Relative Minor",
            "rule_type": "diatonic",
            "source_chord_pattern": "I",
            "target_chord_pattern": "vi",
            "description": "Replace tonic with relative minor",
            "priority": 2,
        },
        {
            "rule_name": "Mediant Substitution",
            "rule_type": "diatonic",
            "source_chord_pattern": "I",
            "target_chord_pattern": "iii",
            "description": "Replace tonic with mediant (share 2 notes)",
            "priority": 2,
        },
    ]

    for rule_data in rules:
        rule = SubstitutionRule(**rule_data)
        db.add(rule)
        print(f"  Added rule: {rule_data['rule_name']}")

    db.commit()
    print(f"Seeded {len(rules)} substitution rules")


def seed_reharmonization_patterns(db):
    """Seed common reharmonization patterns."""
    print("Seeding reharmonization patterns...")

    patterns = [
        {
            "pattern_name": "Jazz II-V-I",
            "original_progression": ["I", "V", "I"],
            "reharmonized_progression": ["IIm7", "V7", "Imaj7"],
            "genre": "jazz",
            "complexity_level": 2,
            "description": "Add ii-V progression before tonic",
        },
        {
            "pattern_name": "Pop Progression Extended",
            "original_progression": ["I", "V", "vi", "IV"],
            "reharmonized_progression": ["Imaj7", "V7", "VIm9", "IVmaj7"],
            "genre": "pop",
            "complexity_level": 3,
            "description": "Extended chords for pop progression",
        },
    ]

    for pattern_data in patterns:
        pattern = ReharmonizationPattern(**pattern_data)
        db.add(pattern)
        print(f"  Added pattern: {pattern_data['pattern_name']}")

    db.commit()
    print(f"Seeded {len(patterns)} reharmonization patterns")


def main():
    """Main seeding function."""
    print("Starting database seeding...")

    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    # Create database session
    db = SessionLocal()

    try:
        # Seed data
        seed_chords(db)
        seed_key_signatures(db)
        seed_substitution_rules(db)
        seed_reharmonization_patterns(db)

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"\nError during seeding: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
