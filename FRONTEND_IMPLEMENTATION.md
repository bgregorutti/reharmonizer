# Frontend Implementation Summary

This document describes the complete frontend implementation for the Reharmonizer application.

## Overview

The frontend is a React + TypeScript application that provides an interactive interface for music reharmonization and improvisation. Users can input music via key signatures (classical), chord lists (modern), or search for chords by note, then get chord substitutions and improvisation notes with visual music notation.

## Architecture

### Technology Stack
- **React 18.2.0** - UI framework
- **TypeScript 5.3.3** - Type safety
- **Vite 5.0.11** - Build tool
- **VexFlow 5.0.0** - Music notation rendering
- **Axios 1.6.5** - API communication
- **React Router DOM 6.21.0** - Routing

### Project Structure
```
frontend/src/
├── components/
│   ├── common/
│   │   └── MusicNotation.tsx          # VexFlow rendering component
│   ├── features/
│   │   ├── KeySignature/
│   │   │   ├── KeySignatureInput.tsx  # Classical mode: key signature selection
│   │   │   └── KeySignatureInput.css
│   │   ├── ChordInput/
│   │   │   ├── ChordListInput.tsx     # Modern mode: chord list input
│   │   │   └── ChordListInput.css
│   │   ├── NoteSearch/
│   │   │   ├── NoteSearchInput.tsx    # Note Search mode: search chords by note
│   │   │   ├── NoteSearchInput.css
│   │   │   ├── ChordSearchResultsDisplay.tsx  # Display search results with notation
│   │   │   └── ChordSearchResultsDisplay.css
│   │   ├── ChordDisplay/
│   │   │   ├── ChordSubstitutionDisplay.tsx  # Shows chord substitutions
│   │   │   └── ChordSubstitutionDisplay.css
│   │   ├── NotesDisplay/
│   │   │   ├── ImprovisationNotesDisplay.tsx  # Shows improvisation notes
│   │   │   └── ImprovisationNotesDisplay.css
│   │   └── ChordSubstitution/
│   │       ├── ChordSubstitutionView.tsx      # Main view combining all components
│   │       └── ChordSubstitutionView.css
├── services/
│   ├── api.ts                         # Axios client configuration
│   ├── chordService.ts                # Chord API service
│   └── reharmonizationService.ts      # Reharmonization API service
└── types/
    ├── chord.ts                       # TypeScript interfaces for chords
    └── api.ts                         # API request/response types

## Features Implemented

### 1. Input Modes

#### Classical Mode (Key Signature)
**Component:** `KeySignatureInput.tsx`

- Select between Major and Minor keys
- Visual grid of all key signatures
- Displays sharps/flats count for each key
- 15 major keys (C, G, D, A, E, B, F#, C#, F, Bb, Eb, Ab, Db, Gb, Cb)
- 15 minor keys (Am, Em, Bm, F#m, C#m, G#m, D#m, A#m, Dm, Gm, Cm, Fm, Bbm, Ebm, Abm)
- Automatically fetches diatonic chords for selected key

**Features:**
- Quality selector (Major/Minor toggle buttons)
- Key grid with visual feedback
- Shows accidental count (sharps/flats)
- Selected key display with signature details

#### Modern Mode (Chord List)
**Component:** `ChordListInput.tsx`

- Free-form chord symbol input
- Autocomplete suggestions from database
- Add/remove chords dynamically
- Visual chord chips display
- Supports all common chord types (maj7, m7, 7, dim, aug, sus4, 6, 9, 13)

**Features:**
- Real-time chord suggestions from backend
- Chord chip display with remove buttons
- Clear all functionality
- Help text with common chord types
- Press Enter to add chord

#### Note Search Mode
**Components:** `NoteSearchInput.tsx`, `ChordSearchResultsDisplay.tsx`

- Search for all chords containing a specific note
- 12-note selector (C through B with sharps)
- Scale type selection (Major/Minor)
- Visual music notation for all matching chords
- Highlights the searched note in each chord

**Features:**
- Interactive note buttons (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
- Scale context selector (Major/Minor)
- Grid display of all matching chords
- VexFlow notation for each chord
- Chord quality badges (major, minor, dominant7, etc.)
- Searched note highlighting in results
- Handles enharmonic equivalents

### 2. Substitution Techniques

**Component:** `ChordSubstitutionView.tsx` (technique selector section)

Five substitution techniques available:
1. **Random** - Random selection from available chords
2. **Tritone Substitution** - Replace with chord a tritone away
3. **Diatonic** - Stay within the key signature
4. **Chromatic Approach** - Use chromatic passing chords
5. **Circle of Fifths** - Follow the circle of fifths progression

**Features:**
- Visual technique cards with descriptions
- Selected technique highlighting
- Technique passed to backend API

### 3. Chord Substitution Display

**Component:** `ChordSubstitutionDisplay.tsx`

Shows:
- Original chord with music notation
- Grid of substitution options (up to 5)
- Each substitution card shows:
  - Chord symbol
  - Technique badge (color-coded)
  - Music notation rendering
  - Description
  - Common usage context
  - Similarity score (0-100%)

**Features:**
- Click any substitution to explore it further
- Color-coded technique badges
- Visual score bars
- Responsive grid layout

### 4. Improvisation Notes Display

**Component:** `ImprovisationNotesDisplay.tsx`

Shows:
- **Recommended Notes** (main focus)
  - 5 selected notes ideal for improvisation
  - Music notation rendering
  - Visual note badges
- **Chord Tones**
  - Notes that make up the chord
  - Safe and strong choices
- **Scale Notes**
  - Notes from appropriate scale
  - Great for melodic passages
- **Avoid Notes** (if any)
  - Notes that may clash
  - Use sparingly

**Features:**
- Visual note badges (color-coded by category)
- Music notation for recommended notes
- Usage tips section
- Clear categorization

### 5. Music Notation Rendering

**Component:** `MusicNotation.tsx`

Uses VexFlow to render:
- Individual notes
- Chord voicings
- Western modern music notation
- Treble clef
- Accidentals (sharps/flats)

**Chord Parsing:**
- Major triads: C, D, E, F, G, A, B
- Minor triads: Cm, Dm, Em, etc.
- Dominant 7th: C7, D7, G7, etc.
- Major 7th: Cmaj7, Dmaj7, etc.
- Minor 7th: Cm7, Dm7, etc.

**Features:**
- Automatic chord voicing (close position, treble clef)
- Note transposition for chord building
- Accidental handling (sharps/flats)
- Configurable width/height

## API Integration

### Endpoints Used

1. **GET /api/v1/chords** - Fetch all chords
2. **GET /api/v1/keys/{key}/chords** - Fetch chords for key signature
3. **GET /api/v1/chords/search/by-note?note={note}&scale_type={scale_type}** - Search chords by note
4. **GET /api/v1/reharmonize/substitutions/{chord}?technique={technique}** - Get substitutions
5. **GET /api/v1/improvisation/notes/{chord}?count={count}** - Get improvisation notes

### API Client Configuration

**File:** `services/api.ts`

- Base URL: `http://localhost:8000/api/v1` (configurable via env var)
- Axios instance with JSON headers
- Error interceptor for logging

## User Flow

### Flow A: Chord Substitution (Classical/Modern modes)

1. **Select Input Mode**
   - Classical (Key Signature) or Modern (Chord List)

2. **Input Music**
   - Classical: Select key signature → Auto-loads diatonic chords
   - Modern: Enter chord symbols manually

3. **Select Technique**
   - Choose substitution technique (Random, Tritone, Diatonic, etc.)

4. **Select Chord to Reharmonize**
   - Click any chord from the list

5. **View Results**
   - See chord substitutions with music notation
   - See improvisation notes with recommendations
   - Click any substitution to explore it

### Flow B: Note Search Mode

1. **Select Note Search Mode**
   - Click "🔍 Note Search" tab

2. **Select Note and Scale**
   - Choose note from C through B (with sharps)
   - Select scale type (Major/Minor)

3. **View Results**
   - See all chords containing that note
   - Visual music notation for each chord
   - Searched note highlighted in results
   - Chord quality badges and full note composition

## Styling

All components use custom CSS with:
- Modern card-based design
- Color-coded elements (techniques, notes, badges)
- Responsive layouts (grid, flexbox)
- Smooth transitions and hover effects
- Mobile-friendly breakpoints

### Color Scheme

- **Primary Blue**: #2196F3 (selections, accents)
- **Green**: #4CAF50 (recommended notes, success)
- **Purple**: #9C27B0 (scale notes)
- **Red**: #f44336 (avoid notes, delete actions)
- **Technique Colors**:
  - Tritone: #ff6b6b
  - Diatonic: #4ecdc4
  - Chromatic: #95e1d3
  - Circle of 5ths: #f9ca24
  - Random: #a29bfe

## State Management

Uses React hooks for local state:
- `useState` for component state
- No global state management (could add Context API if needed)

**Main State Variables:**
- `inputMode`: 'key' | 'chords'
- `selectedKey`: string
- `selectedChords`: string[]
- `selectedTechnique`: Technique enum
- `currentChord`: string
- `substitutions`: SubstitutionOption[]
- `improvisationNotes`: ImprovisationNotesResponse
- `loading`: boolean
- `error`: string | null

## TypeScript Interfaces

### Chord Types
```typescript
interface Chord {
  id?: number;
  symbol: string;
  root_note: string;
  notes: string[];
  intervals: string[];
  chord_quality?: string;
}

interface SubstitutionOption {
  chord: string;
  technique: string;
  description: string;
  common_usage?: string;
  score: number;
}

interface SubstitutionResponse {
  original_chord: string;
  substitutions: SubstitutionOption[];
}

interface ImprovisationNotesResponse {
  chord_symbol: string;
  chord_tones: string[];
  scale_notes: string[];
  recommended_notes: string[];
  avoid_notes: string[];
}
```

## Running the Frontend

### Development
```bash
cd frontend
npm install
npm run dev
```

Access at: http://localhost:5173

### Docker
```bash
docker-compose up frontend
```

## Future Enhancements

Possible improvements:
1. Save/load chord progressions
2. Export to MusicXML or MIDI
3. Playback audio preview
4. Custom key signatures
5. More advanced notation (bass clef, different time signatures)
6. Progression analysis visualization
7. User preferences (favorite techniques)
8. Undo/redo functionality

## Testing

To test the complete flow:
1. Navigate to http://localhost:5173
2. Try both input modes (Classical and Modern)
3. Select different techniques
4. Click chords to see substitutions and notes
5. Verify music notation renders correctly
6. Check mobile responsiveness

## Notes

- All components are fully typed with TypeScript
- VexFlow renders music notation dynamically
- API integration uses async/await pattern
- Error handling with try/catch and user feedback
- Loading states for better UX
- Responsive design for mobile and desktop
