# Reharmonizer Core

Core music theory and chord substitution algorithms for the Reharmonizer application.

## Overview

This package provides the fundamental music theory logic and chord/note recommendation algorithms used by the Reharmonizer web application. It's designed to be independent of the web framework and can be used in other music theory applications.

## Features

- **Chord Recommendations**: Suggest alternative chords based on music theory rules
- **Note Recommendations**: Suggest improvisation notes for given chords
- **Music21 Integration**: Wrapper around music21 for music theory operations
- **Theory Utilities**: Chord analysis, scale generation, interval calculations

## Installation

```bash
# Install with uv
uv pip install -e .

# Install with pip
pip install -e .
```

## Usage

### Chord Recommendations

```python
from reharmonizer_core.substitution import ChordRecommender

recommender = ChordRecommender()
suggestions = recommender.recommend_chords("C7", available_chords=["Db7", "Em", "Am", "G7", "F#dim"])
# Returns 5 random chord suggestions
```

### Note Recommendations

```python
from reharmonizer_core.substitution import NoteRecommender

recommender = NoteRecommender()
notes = recommender.recommend_notes("Cmaj7")
# Returns: {
#   "chord_tones": ["C", "E", "G", "B"],
#   "scale_notes": ["C", "D", "E", "F", "G", "A", "B"],
#   "recommended_notes": ["D", "G", "A", ...],  # 5 random suggestions
# }
```

## Architecture

```
reharmonizer_core/
├── substitution/          # Chord and note recommendation algorithms
│   ├── chord_recommender.py
│   └── note_recommender.py
├── theory/                # Music theory utilities
│   ├── chord_analyzer.py
│   └── scale_generator.py
└── music21_integration/   # Music21 wrapper
    └── converter.py
```

## Implementation Strategy

### Current (Simple) Implementation

The current implementation uses a simple random selection approach:

1. **Chord Recommendations**: Randomly select 5 chords from available database chords
2. **Note Recommendations**: Extract chord tones and scale notes, randomly select 5 notes

This provides immediate functionality while keeping the implementation simple.

### Future: Similarity Score (Planned)

A more sophisticated approach will use similarity scoring based on:
- Shared notes between chords
- Interval relationships
- Harmonic function similarity
- Voice leading quality
- Genre-specific preferences

See the main project README for the similarity score implementation plan.

## Development

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=reharmonizer_core
```

## License

[Same as main project]
