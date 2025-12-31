"""
Functional Harmony Substitution Generator

This script analyzes chord relationships based on functional harmony theory
and generates precise substitutions (dominant, subdominant, mediant, submediant, leading tone)
rather than generic "diatonic" substitutions.

Functional harmony relationships:
- Mediant:      3, 5, 7 → 1, 3, 5  (3 common notes)
- Subdominant:  1, 3    → 5, 7     (2 common notes)
- Dominant:     5, 7    → 1, 3     (2 common notes)
- Submediant:   1, 3, 5 → 3, 5, 7  (3 common notes)
- Leading tone: 7       → 1        (1 common note)
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Chord, ChordSubstitution
from music21 import harmony


# Functional harmony specifications
FUNCTIONAL_SPECS = {
    "mediant": {
        "nr_common_notes": 3,
        "source_positions": ["third", "fifth", "seventh"],
        "target_positions": ["root", "third", "fifth"],
        "description": "Mediant relationship",
        "score": 0.85,
        "usage_context": "classical"
    },
    "subdominant": {
        "nr_common_notes": 2,
        "source_positions": ["root", "third"],
        "target_positions": ["fifth", "seventh"],
        "description": "Subdominant relationship",
        "score": 0.90,
        "usage_context": "classical"
    },
    "dominant": {
        "nr_common_notes": 2,
        "source_positions": ["fifth", "seventh"],
        "target_positions": ["root", "third"],
        "description": "Dominant relationship",
        "score": 0.95,
        "usage_context": "classical"
    },
    "submediant": {
        "nr_common_notes": 3,
        "source_positions": ["root", "third", "fifth"],
        "target_positions": ["third", "fifth", "seventh"],
        "description": "Submediant relationship",
        "score": 0.85,
        "usage_context": "classical"
    },
    "leading_tone": {
        "nr_common_notes": 1,
        "source_positions": ["seventh"],
        "target_positions": ["root"],
        "description": "Leading tone relationship",
        "score": 0.80,
        "usage_context": "classical"
    }
}


def normalize_note(note_name):
    """Normalize note name by removing octave and converting accidentals."""
    note_name = note_name.replace("♭", "-").replace("♯", "#")
    base_note = note_name.rstrip("0123456789")
    return base_note


def get_chord_position_map(chord_symbol):
    """
    Map each note in a chord to its functional position.
    Returns: dict mapping note_name -> position_name
    """
    try:
        cs = harmony.ChordSymbol(chord_symbol)
        pitch_names = cs.pitchNames

        # Map positions based on number of notes in chord
        position_map = {}
        positions = ["root", "third", "fifth", "seventh", "ninth", "eleventh", "thirteenth"]

        for i, note in enumerate(pitch_names):
            if i < len(positions):
                normalized_note = normalize_note(note)
                position_map[normalized_note] = positions[i]

        return position_map
    except Exception as e:
        print(f"  Warning: Could not parse chord symbol {chord_symbol}: {e}")
        return {}


def check_functional_relationship(source_chord, target_chord, spec):
    """
    Check if a chord pair matches a functional harmony specification.

    Returns:
        bool: True if the relationship matches the spec
        list: Matched common notes with their positions
    """
    # Get position maps for both chords
    source_map = get_chord_position_map(source_chord.symbol)
    target_map = get_chord_position_map(target_chord.symbol)

    if not source_map or not target_map:
        return False, []

    # Find common notes and check if they match the required positions
    matched_notes = []

    for source_note, source_pos in source_map.items():
        if source_note in target_map:
            target_pos = target_map[source_note]

            # Check if this common note matches any required position pair
            for i, src_pos_required in enumerate(spec["source_positions"]):
                tgt_pos_required = spec["target_positions"][i]

                if source_pos == src_pos_required and target_pos == tgt_pos_required:
                    matched_notes.append({
                        "note": source_note,
                        "source_position": source_pos,
                        "target_position": target_pos
                    })
                    break

    # Check if we have the required number of common notes
    if len(matched_notes) >= spec["nr_common_notes"]:
        return True, matched_notes

    return False, []


def analyze_all_substitutions():
    """Analyze all chord pairs and find functional harmony relationships."""
    db = SessionLocal()

    try:
        # Load all chords
        chords = db.query(Chord).all()
        print(f"Loaded {len(chords)} chords from database\n")

        # Store results
        results = {func_type: [] for func_type in FUNCTIONAL_SPECS.keys()}
        total_matches = 0

        # Analyze all chord pairs
        for source_chord in chords:
            for target_chord in chords:
                if source_chord.id == target_chord.id:
                    continue

                # Check each functional relationship
                for func_type, spec in FUNCTIONAL_SPECS.items():
                    is_match, matched_notes = check_functional_relationship(
                        source_chord, target_chord, spec
                    )

                    if is_match:
                        results[func_type].append({
                            "source": source_chord.symbol,
                            "target": target_chord.symbol,
                            "matched_notes": matched_notes
                        })
                        total_matches += 1

        # Print results
        print("=" * 80)
        print("FUNCTIONAL HARMONY SUBSTITUTION ANALYSIS")
        print("=" * 80)

        for func_type, matches in results.items():
            if matches:
                print(f"\n{func_type.upper()} ({len(matches)} matches)")
                print("-" * 80)

                # Show first 10 examples
                for match in matches[:10]:
                    print(f"  {match['source']:10} → {match['target']:10}", end="")
                    note_info = ", ".join([
                        f"{n['note']}({n['source_position']}→{n['target_position']})"
                        for n in match['matched_notes']
                    ])
                    print(f"  Common: {note_info}")

                if len(matches) > 10:
                    print(f"  ... and {len(matches) - 10} more")

        print("\n" + "=" * 80)
        print(f"TOTAL MATCHES: {total_matches}")
        print("=" * 80)

        return results

    finally:
        db.close()


def generate_functional_substitutions():
    """Generate and save functional harmony substitutions to database."""
    db = SessionLocal()

    try:
        # Load all chords
        chords = db.query(Chord).all()

        print(f"Generating functional harmony substitutions for {len(chords)} chords...\n")

        all_substitutions = []
        technique_counts = {}

        # Analyze all chord pairs
        for source_chord in chords:
            for target_chord in chords:
                if source_chord.id == target_chord.id:
                    continue

                # Check each functional relationship
                for func_type, spec in FUNCTIONAL_SPECS.items():
                    is_match, matched_notes = check_functional_relationship(
                        source_chord, target_chord, spec
                    )

                    if is_match:
                        # Create description with matched notes
                        note_info = ", ".join([
                            f"{n['note']}({n['source_position']}→{n['target_position']})"
                            for n in matched_notes
                        ])

                        description = f"{spec['description']}: {note_info}"

                        # Create substitution
                        chord_sub = ChordSubstitution(
                            source_chord_id=source_chord.id,
                            target_chord_id=target_chord.id,
                            technique=func_type,
                            score=spec["score"],
                            description=description,
                            usage_context=spec["usage_context"],
                            relationship_type="functional_harmony"
                        )

                        all_substitutions.append(chord_sub)
                        technique_counts[func_type] = technique_counts.get(func_type, 0) + 1

        # Save to database
        if all_substitutions:
            db.bulk_save_objects(all_substitutions)
            db.commit()

            print(f"\n✓ Generated {len(all_substitutions)} functional harmony substitutions")
            print("\nBreakdown by technique:")
            for technique, count in sorted(technique_counts.items()):
                print(f"  {technique}: {count}")
        else:
            print("\n⚠ No functional harmony substitutions found")

        return all_substitutions

    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Functional Harmony Substitution Analysis")
    parser.add_argument("--analyze", action="store_true", help="Analyze and display relationships")
    parser.add_argument("--generate", action="store_true", help="Generate and save to database")

    args = parser.parse_args()

    if args.generate:
        generate_functional_substitutions()
    else:
        # Default: analyze
        analyze_all_substitutions()
