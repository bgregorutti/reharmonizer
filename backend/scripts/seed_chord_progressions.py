"""
Seed chord progression patterns into the database.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.chord_progression import ChordProgressionPattern


def seed_jazz_patterns(db):
    """Seed jazz chord progression patterns."""
    jazz_patterns = [
        {
            "name": "ii-V-I",
            "style": "jazz",
            "roman_numeral_sequence": ["ii7", "V7", "Imaj7"],
            "example_chords": ["Dm7", "G7", "Cmaj7"],
            "description": "The most fundamental jazz progression",
            "usage_context": "Cadence, turnaround, endings",
            "popularity_score": 1.0,
            "min_length": 3,
            "max_length": 3,
            "is_repeatable": 1,
        },
        {
            "name": "I-vi-ii-V",
            "style": "jazz",
            "roman_numeral_sequence": ["Imaj7", "vi7", "ii7", "V7"],
            "example_chords": ["Cmaj7", "Am7", "Dm7", "G7"],
            "description": "Classic jazz turnaround",
            "usage_context": "Turnaround, repeated sections",
            "popularity_score": 0.9,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "Minor ii-V-i",
            "style": "jazz",
            "roman_numeral_sequence": ["ii7b5", "V7", "im7"],
            "example_chords": ["Dm7b5", "G7", "Cm7"],
            "description": "Minor key ii-V-i progression",
            "usage_context": "Minor key cadence",
            "popularity_score": 0.85,
            "min_length": 3,
            "max_length": 3,
            "is_repeatable": 1,
        },
        {
            "name": "Blues progression",
            "style": "jazz",
            "roman_numeral_sequence": ["I7", "I7", "I7", "I7", "IV7", "IV7", "I7", "I7", "V7", "IV7", "I7", "V7"],
            "example_chords": ["C7", "C7", "C7", "C7", "F7", "F7", "C7", "C7", "G7", "F7", "C7", "G7"],
            "description": "12-bar blues progression",
            "usage_context": "Blues form, jazz standards",
            "popularity_score": 0.95,
            "min_length": 12,
            "max_length": 12,
            "is_repeatable": 1,
        },
        {
            "name": "Rhythm changes A",
            "style": "jazz",
            "roman_numeral_sequence": ["Imaj7", "vi7", "ii7", "V7", "iii7", "vi7", "ii7", "V7"],
            "example_chords": ["Cmaj7", "Am7", "Dm7", "G7", "Em7", "Am7", "Dm7", "G7"],
            "description": "First 8 bars of rhythm changes",
            "usage_context": "Jazz standards, bebop",
            "popularity_score": 0.8,
            "min_length": 8,
            "max_length": 8,
            "is_repeatable": 0,
        },
        {
            "name": "Jazz minor ii-V",
            "style": "jazz",
            "roman_numeral_sequence": ["ii7", "V7"],
            "example_chords": ["Dm7", "G7"],
            "description": "Two-chord jazz progression",
            "usage_context": "Bridge, transitions",
            "popularity_score": 0.75,
            "min_length": 2,
            "max_length": 2,
            "is_repeatable": 1,
        },
    ]

    for pattern_data in jazz_patterns:
        pattern = ChordProgressionPattern(**pattern_data)
        db.add(pattern)

    print(f"Added {len(jazz_patterns)} jazz patterns")


def seed_pop_patterns(db):
    """Seed pop chord progression patterns."""
    pop_patterns = [
        {
            "name": "I-V-vi-IV",
            "style": "pop",
            "roman_numeral_sequence": ["I", "V", "vi", "IV"],
            "example_chords": ["C", "G", "Am", "F"],
            "description": "The most popular pop progression of all time",
            "usage_context": "Verse, chorus, entire song",
            "popularity_score": 1.0,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "I-IV-V",
            "style": "pop",
            "roman_numeral_sequence": ["I", "IV", "V"],
            "example_chords": ["C", "F", "G"],
            "description": "Classic three-chord pop progression",
            "usage_context": "Verse, chorus",
            "popularity_score": 0.95,
            "min_length": 3,
            "max_length": 3,
            "is_repeatable": 1,
        },
        {
            "name": "vi-IV-I-V",
            "style": "pop",
            "roman_numeral_sequence": ["vi", "IV", "I", "V"],
            "example_chords": ["Am", "F", "C", "G"],
            "description": "Popular alternative to I-V-vi-IV",
            "usage_context": "Verse, pre-chorus",
            "popularity_score": 0.9,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "I-vi-IV-V",
            "style": "pop",
            "roman_numeral_sequence": ["I", "vi", "IV", "V"],
            "example_chords": ["C", "Am", "F", "G"],
            "description": "50s progression (doo-wop)",
            "usage_context": "Verse, nostalgic feel",
            "popularity_score": 0.85,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "I-IV-vi-V",
            "style": "pop",
            "roman_numeral_sequence": ["I", "IV", "vi", "V"],
            "example_chords": ["C", "F", "Am", "G"],
            "description": "Common pop ballad progression",
            "usage_context": "Ballads, slower songs",
            "popularity_score": 0.8,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "I-V-IV",
            "style": "pop",
            "roman_numeral_sequence": ["I", "V", "IV"],
            "example_chords": ["C", "G", "F"],
            "description": "Simple three-chord pop",
            "usage_context": "Verse, simple songs",
            "popularity_score": 0.75,
            "min_length": 3,
            "max_length": 3,
            "is_repeatable": 1,
        },
    ]

    for pattern_data in pop_patterns:
        pattern = ChordProgressionPattern(**pattern_data)
        db.add(pattern)

    print(f"Added {len(pop_patterns)} pop patterns")


def seed_classical_patterns(db):
    """Seed classical chord progression patterns."""
    classical_patterns = [
        {
            "name": "I-IV-V-I",
            "style": "classical",
            "roman_numeral_sequence": ["I", "IV", "V", "I"],
            "example_chords": ["C", "F", "G", "C"],
            "description": "Perfect authentic cadence",
            "usage_context": "Phrase endings, strong resolution",
            "popularity_score": 1.0,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 0,
        },
        {
            "name": "I-ii-V-I",
            "style": "classical",
            "roman_numeral_sequence": ["I", "ii", "V", "I"],
            "example_chords": ["C", "Dm", "G", "C"],
            "description": "Subdominant approach to cadence",
            "usage_context": "Phrase structure, classical",
            "popularity_score": 0.9,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 0,
        },
        {
            "name": "I-vi-ii-V",
            "style": "classical",
            "roman_numeral_sequence": ["I", "vi", "ii", "V"],
            "example_chords": ["C", "Am", "Dm", "G"],
            "description": "Circle of fifths progression",
            "usage_context": "Extended phrases",
            "popularity_score": 0.85,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
        {
            "name": "I-IV-I-V",
            "style": "classical",
            "roman_numeral_sequence": ["I", "IV", "I", "V"],
            "example_chords": ["C", "F", "C", "G"],
            "description": "Simple functional harmony",
            "usage_context": "Basic phrase structure",
            "popularity_score": 0.8,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 0,
        },
        {
            "name": "I-V-vi-iii-IV-I-IV-V",
            "style": "classical",
            "roman_numeral_sequence": ["I", "V", "vi", "iii", "IV", "I", "IV", "V"],
            "example_chords": ["C", "G", "Am", "Em", "F", "C", "F", "G"],
            "description": "Pachelbel's Canon progression",
            "usage_context": "Extended sequences",
            "popularity_score": 0.9,
            "min_length": 8,
            "max_length": 8,
            "is_repeatable": 1,
        },
        {
            "name": "I-vi-IV-V",
            "style": "classical",
            "roman_numeral_sequence": ["I", "vi", "IV", "V"],
            "example_chords": ["C", "Am", "F", "G"],
            "description": "Classical harmonic sequence",
            "usage_context": "Phrase progression",
            "popularity_score": 0.75,
            "min_length": 4,
            "max_length": 4,
            "is_repeatable": 1,
        },
    ]

    for pattern_data in classical_patterns:
        pattern = ChordProgressionPattern(**pattern_data)
        db.add(pattern)

    print(f"Added {len(classical_patterns)} classical patterns")


def main():
    """Main function to seed all chord progression patterns."""
    db = SessionLocal()

    try:
        # Clear existing patterns
        print("Clearing existing chord progression patterns...")
        db.query(ChordProgressionPattern).delete()
        db.commit()

        # Seed jazz patterns
        print("\nSeeding jazz patterns...")
        seed_jazz_patterns(db)

        # Seed pop patterns
        print("\nSeeding pop patterns...")
        seed_pop_patterns(db)

        # Seed classical patterns
        print("\nSeeding classical patterns...")
        seed_classical_patterns(db)

        # Commit all changes
        db.commit()
        print("\n✅ Successfully seeded chord progression patterns!")

        # Show counts
        total = db.query(ChordProgressionPattern).count()
        jazz_count = db.query(ChordProgressionPattern).filter_by(style="jazz").count()
        pop_count = db.query(ChordProgressionPattern).filter_by(style="pop").count()
        classical_count = db.query(ChordProgressionPattern).filter_by(style="classical").count()

        print(f"\nTotal patterns: {total}")
        print(f"Jazz: {jazz_count}")
        print(f"Pop: {pop_count}")
        print(f"Classical: {classical_count}")

    except Exception as e:
        print(f"❌ Error seeding chord progressions: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
