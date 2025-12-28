# Similarity Score Implementation Plan

## Overview

The similarity score algorithm will replace the current random selection approach with intelligent chord and note recommendations based on music theory principles. The score will range from 0.0 (not related) to 1.0 (highly related).

## Goals

1. **Better Recommendations**: Suggest chords that sound musically related
2. **Ranked Results**: Order suggestions from most to least similar
3. **Explainability**: Provide reasoning for why a chord was recommended
4. **Flexibility**: Allow weighting of different factors based on genre or style

## Similarity Factors

### 1. Shared Notes Score (Weight: 0.35)

**Formula**: `shared_notes_count / max(chord1_notes_count, chord2_notes_count)`

**Example**:
- `Cmaj7` = [C, E, G, B]
- `Am7` = [A, C, E, G]
- Shared notes: [C, E, G] = 3 notes
- Score: 3/4 = 0.75

**Implementation**:
```python
def calculate_shared_notes_score(chord1_notes, chord2_notes):
    shared = set(chord1_notes).intersection(set(chord2_notes))
    max_notes = max(len(chord1_notes), len(chord2_notes))
    return len(shared) / max_notes if max_notes > 0 else 0
```

### 2. Root Movement Score (Weight: 0.25)

Strong chord progressions often move by specific intervals:
- **Perfect 5th/4th**: 1.0 (strongest, e.g., C → G)
- **Minor 2nd (chromatic)**: 0.9 (e.g., C → Db)
- **Major 2nd**: 0.8 (e.g., C → D)
- **Minor 3rd**: 0.7 (e.g., C → Eb)
- **Major 3rd**: 0.6 (e.g., C → E)
- **Tritone**: 0.5 (e.g., C → F# - special case for tritone sub)
- **Other intervals**: 0.3

**Implementation**:
```python
INTERVAL_SCORES = {
    0: 0.5,   # Same root (less interesting)
    1: 0.9,   # Minor 2nd (chromatic)
    2: 0.8,   # Major 2nd
    3: 0.7,   # Minor 3rd
    4: 0.6,   # Major 3rd
    5: 1.0,   # Perfect 4th
    6: 0.5,   # Tritone (special case)
    7: 1.0,   # Perfect 5th
    8: 0.7,   # Minor 6th
    9: 0.6,   # Major 6th
    10: 0.8,  # Minor 7th
    11: 0.9,  # Major 7th
}

def calculate_root_movement_score(root1, root2):
    # Calculate semitone distance between roots
    interval = calculate_semitone_distance(root1, root2)
    return INTERVAL_SCORES.get(interval, 0.3)
```

### 3. Harmonic Function Score (Weight: 0.20)

Chords with similar harmonic functions are more interchangeable:
- **Same function**: 1.0 (e.g., both tonic)
- **Related function**: 0.6 (e.g., tonic ↔ pre-dominant)
- **Different function**: 0.3

**Harmonic Functions**:
- **Tonic**: I, iii, vi (stability, resolution)
- **Pre-dominant**: ii, IV (preparation for dominant)
- **Dominant**: V, vii° (tension, wants to resolve to tonic)

**Implementation**:
```python
HARMONIC_FUNCTIONS = {
    "major": "tonic",
    "major7": "tonic",
    "minor": "tonic",  # Context-dependent
    "minor7": "pre-dominant",  # Often ii or vi
    "dominant7": "dominant",
}

def calculate_function_score(quality1, quality2):
    func1 = HARMONIC_FUNCTIONS.get(quality1, "unknown")
    func2 = HARMONIC_FUNCTIONS.get(quality2, "unknown")

    if func1 == func2:
        return 1.0
    elif func1 != "unknown" and func2 != "unknown":
        return 0.6  # Related but different
    else:
        return 0.3
```

### 4. Voice Leading Score (Weight: 0.20)

Smooth voice leading makes chord transitions sound better:
- **All voices move ≤ 2 semitones**: 1.0 (excellent)
- **Average movement ≤ 2 semitones**: 0.8 (good)
- **Average movement ≤ 4 semitones**: 0.6 (acceptable)
- **Average movement > 4 semitones**: 0.3 (weak)

**Implementation**:
```python
def calculate_voice_leading_score(chord1_notes, chord2_notes):
    # For each note in chord1, find closest note in chord2
    movements = []
    for note1 in chord1_notes:
        min_movement = min(
            abs(semitone_distance(note1, note2))
            for note2 in chord2_notes
        )
        movements.append(min_movement)

    avg_movement = sum(movements) / len(movements)
    max_movement = max(movements)

    # Bonus for stepwise motion
    if max_movement <= 2:
        return 1.0
    elif avg_movement <= 2:
        return 0.8
    elif avg_movement <= 4:
        return 0.6
    else:
        return 0.3
```

## Combined Score Calculation

**Formula**:
```
similarity_score = (
    shared_notes_score * 0.35 +
    root_movement_score * 0.25 +
    harmonic_function_score * 0.20 +
    voice_leading_score * 0.20
)
```

**Example Calculation**:

For `C7` → `Db7` (tritone substitution):
- Shared notes: [F, B♭] = 2/4 = 0.50 × 0.35 = 0.175
- Root movement: Tritone = 0.5 × 0.25 = 0.125
- Harmonic function: Both dominant = 1.0 × 0.20 = 0.200
- Voice leading: (Assuming smooth) = 0.8 × 0.20 = 0.160
- **Total**: 0.175 + 0.125 + 0.200 + 0.160 = **0.66**

## Implementation Steps

### Phase 1: Core Algorithm (Week 1-2)

1. **Create similarity scoring module** in `reharmonizer-core`:
   ```
   reharmonizer_core/
   └── scoring/
       ├── __init__.py
       ├── similarity_scorer.py
       ├── shared_notes.py
       ├── root_movement.py
       ├── harmonic_function.py
       └── voice_leading.py
   ```

2. **Implement individual scoring functions**:
   - `shared_notes.py`: Calculate shared notes between chords
   - `root_movement.py`: Score based on interval between roots
   - `harmonic_function.py`: Determine and compare harmonic functions
   - `voice_leading.py`: Analyze voice leading quality

3. **Create main scorer class**:
   ```python
   class SimilarityScorer:
       def score(self, chord1, chord2, context=None):
           """Calculate similarity score between two chords."""
           pass

       def rank_candidates(self, source_chord, candidates):
           """Rank candidate chords by similarity."""
           pass
   ```

### Phase 2: Integration (Week 3)

1. **Update `ChordRecommender`** to use similarity scoring:
   ```python
   def recommend_chords(self, source_chord, available_chords, count=5):
       scorer = SimilarityScorer()

       # Score all candidates
       scored = [
           {
               **chord,
               "score": scorer.score(source_chord, chord),
               "score_breakdown": scorer.get_breakdown(source_chord, chord)
           }
           for chord in available_chords
       ]

       # Sort by score (highest first)
       scored.sort(key=lambda x: x["score"], reverse=True)

       return scored[:count]
   ```

2. **Add technique-specific scoring**:
   - Tritone: Boost score for tritone interval
   - Diatonic: Boost score for same-key chords
   - Chromatic: Boost score for chromatic approach

### Phase 3: Context-Aware Scoring (Week 4)

1. **Add context parameters**:
   ```python
   def score(self, chord1, chord2, context=None):
       # context = {
       #     "key": "C major",
       #     "previous_chord": "Dm7",
       #     "next_chord": "G7",
       #     "position": "ii",
       #     "genre": "jazz"
       # }
   ```

2. **Implement context adjustments**:
   - Key context: Boost diatonic chords
   - Progression context: Consider surrounding chords
   - Genre context: Weight factors differently (jazz vs pop)

### Phase 4: Testing & Refinement (Week 5)

1. **Create test suite** with known good substitutions:
   - ii-V-I progression variations
   - Common jazz substitutions
   - Pop/rock progressions

2. **Validate scores** against music theory expectations

3. **Tune weights** based on musical results

## Advanced Features (Future)

### Genre-Specific Weights

```python
GENRE_WEIGHTS = {
    "jazz": {
        "shared_notes": 0.25,
        "root_movement": 0.25,
        "harmonic_function": 0.20,
        "voice_leading": 0.30,  # More important in jazz
    },
    "pop": {
        "shared_notes": 0.40,  # More emphasis on common notes
        "root_movement": 0.30,
        "harmonic_function": 0.20,
        "voice_leading": 0.10,
    },
}
```

### Machine Learning Enhancement

Train a model on:
- Labeled chord progressions (good/bad substitutions)
- Real song chord progressions
- User feedback on recommendations

Use the ML model to refine weights or add additional factors.

## Success Metrics

1. **Qualitative**: Do the top 3 recommendations sound musically appropriate?
2. **Consistency**: Do similar chords get similar scores?
3. **Technique Alignment**: Do tritone subs score high with tritone technique?
4. **User Feedback**: Allow users to rate recommendations

## Example Expected Results

### C7 Substitutions (Jazz Context)

1. **Db7** - Score: 0.85 (Tritone substitution, shares tritone)
2. **A7** - Score: 0.78 (Secondary dominant, smooth voice leading)
3. **C7#9** - Score: 0.75 (Same root, extended harmony)
4. **Gm7** - Score: 0.65 (Related ii chord)
5. **E♭7** - Score: 0.60 (Chromatic approach)

### Cmaj7 Substitutions (Pop Context)

1. **Am7** - Score: 0.82 (Relative minor, shares 3 notes)
2. **Em7** - Score: 0.75 (iii chord, diatonic)
3. **Fmaj7** - Score: 0.70 (IV chord, strong progression)
4. **C6** - Score: 0.68 (Same function, similar sound)
5. **G** - Score: 0.62 (Dominant, common progression)

## References

- Music theory textbooks on harmonic function
- Jazz theory books (Mark Levine's "Jazz Theory Book")
- Voice leading principles (classical counterpoint)
- Empirical analysis of popular chord progressions

## Timeline

- **Week 1-2**: Core algorithm implementation
- **Week 3**: Integration with existing code
- **Week 4**: Context-aware enhancements
- **Week 5**: Testing and refinement
- **Week 6+**: Advanced features and ML exploration
