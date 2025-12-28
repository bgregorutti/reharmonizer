# Chord Substitution Database System

## Overview

The reharmonizer now uses a **music theory-based chord substitution database** instead of random selection. Each chord has pre-computed substitution options based on established music theory principles.

## Database Schema

### ChordSubstitution Table

Stores relationships between source chords and their valid substitutions:

```
chord_substitutions
├── source_chord_id (FK -> chords.id)
├── target_chord_id (FK -> chords.id)
├── technique (string)
├── score (float 0.0-1.0)
├── description (text)
├── usage_context (string)
└── relationship_type (string)
```

## Substitution Techniques

### 1. **Tritone Substitution** (technique: `tritone`)
- **Theory**: Replace a dominant 7th chord with another dominant 7th chord a tritone (6 semitones) away
- **Example**: C7 → F#7 (Gb7)
- **Why it works**: Both chords share the same tritone (3rd and 7th notes)
- **Score**: 0.95
- **Usage**: Jazz

### 2. **Diatonic Substitution** (technique: `diatonic`)
- **Theory**: Chords that share common tones within the same key
- **Examples**:
  - I ↔ iii (share 2 notes)
  - I ↔ vi (share 2 notes)
  - ii ↔ IV (share 2 notes)
- **Score**: 0.5 - 0.9 (based on number of shared notes)
- **Usage**: Classical, all genres

### 3. **Relative Substitution** (technique: `relative`)
- **Theory**: Major chord ↔ its relative minor (3 semitones down)
- **Example**: C major ↔ A minor
- **Why it works**: Share the same key signature
- **Score**: 0.90
- **Usage**: Classical

### 4. **Parallel Substitution** (technique: `parallel`)
- **Theory**: Same root note, different quality (major ↔ minor)
- **Example**: C major ↔ C minor
- **Score**: 0.75
- **Usage**: Pop, modal interchange

### 5. **Circle of Fifths** (technique: `circle_fifths`)
- **Theory**: Chords related by fifth intervals
- **Examples**:
  - C → G (up a 5th)
  - C → F (down a 5th / up a 4th)
- **Score**: 0.85 (same quality), 0.70 (different quality)
- **Usage**: Jazz, all genres

### 6. **Chromatic Substitution** (technique: `chromatic`)
- **Theory**: Approach chords a semitone above or below
- **Example**: C7 → C#7 → D7 (chromatic approach)
- **Score**: 0.80 (dominant 7th), 0.70 (same quality), 0.60 (other)
- **Usage**: Jazz, bebop

## Current Database Statistics

With the current seed data (10 chords: C, Dm, Em, F, G, Am, Bdim, Cmaj7, Dm7, G7):

- **Total substitutions**: 82 relationships
- **Breakdown**:
  - Diatonic: 42 relationships
  - Circle of fifths: 28 relationships
  - Chromatic: 6 relationships
  - Relative: 6 relationships

## Usage

### API Endpoint

```http
GET /api/v1/reharmonize/substitutions/{chord_symbol}?technique={technique}
```

**Parameters**:
- `chord_symbol`: The source chord (e.g., "C", "G7", "Cmaj7")
- `technique`: Optional filter (e.g., "diatonic", "tritone", "circle_fifths", "random")

### Example Requests

```bash
# Get diatonic substitutions for C
curl "http://localhost:8000/api/v1/reharmonize/substitutions/C?technique=diatonic"

# Get circle of fifths substitutions for G7
curl "http://localhost:8000/api/v1/reharmonize/substitutions/G7?technique=circle_fifths"

# Get all available substitutions (best scored first)
curl "http://localhost:8000/api/v1/reharmonize/substitutions/C?technique=random"
```

### Example Response

```json
{
  "original_chord": "C",
  "substitutions": [
    {
      "chord": "Em",
      "technique": "diatonic",
      "description": "Shares 2 common tone(s) with C",
      "common_usage": "Alternative to C",
      "score": 0.9
    },
    {
      "chord": "Am",
      "technique": "relative",
      "description": "Relative major/minor: C and Am share the same key signature",
      "common_usage": "Alternative to C",
      "score": 0.9
    }
  ]
}
```

## Generation Process

### 1. Database Setup

```bash
# Seed the database with chords
docker-compose exec backend python scripts/seed_database.py

# Generate substitution relationships
docker-compose exec backend python scripts/generate_substitutions.py
```

### 2. How Substitutions are Generated

The `scripts/generate_substitutions.py` script:

1. Loads all chords from the database
2. For each chord, applies 6 substitution algorithms
3. Generates relationships based on music theory rules
4. Assigns scores based on substitution quality
5. Stores all relationships in the `chord_substitutions` table

### 3. Backend Implementation

The `ReharmonizationEngine` (backend/app/services/reharmonization/engine.py):

1. Queries the database for pre-computed substitutions
2. Filters by technique if specified
3. Orders by score (best first)
4. Falls back to random selection if no theory-based substitution exists

## Expanding the Database

To add more chords and substitutions:

1. Add more chords to `scripts/seed_database.py`
2. Run the seed script
3. Run the substitution generation script
4. The system will automatically compute all substitution relationships

## Future Enhancements

- Add more complex chords (9th, 11th, 13th, altered dominants)
- Implement context-aware substitutions based on chord progressions
- Add genre-specific substitution preferences
- Include voice leading quality scores
- Add tension/resolution analysis
