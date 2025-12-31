# Reharmonizer API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Important Notes

### Trailing Slashes
FastAPI redirects requests without trailing slashes to URLs with trailing slashes (HTTP 307). To avoid redirects:
- Use trailing slashes: `/chords/` instead of `/chords`
- Or use `-L` flag with curl to follow redirects: `curl -L http://localhost:8000/api/v1/chords`

### CORS
The API accepts requests from:
- http://localhost:5173 (frontend)
- http://localhost:3000 (alternative frontend)

## Endpoints

### 1. Chord Endpoints

#### Get All Chords
```bash
GET /chords/
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)

**Example:**
```bash
curl "http://localhost:8000/api/v1/chords/?skip=0&limit=5"
```

**Response:**
```json
[
  {
    "symbol": "C",
    "root_note": "C",
    "notes": ["C", "E", "G"],
    "intervals": [0, 4, 7],
    "chord_quality": "major",
    "id": 1,
    "roman_numeral": null,
    "function": null,
    "created_at": "2025-12-28T14:03:12.922182Z"
  }
]
```

---

#### Search Chords by Note
```bash
GET /chords/search/by-note
```

**Query Parameters:**
- `note` (string, required): The note to search for (e.g., "C", "D#", "Eb")
- `scale_type` (string, optional): Scale context - "major" or "minor" (default: "major")

**Example:**
```bash
# Search for all chords containing C
curl "http://localhost:8000/api/v1/chords/search/by-note?note=C&scale_type=major"

# Search for all chords containing D#
curl "http://localhost:8000/api/v1/chords/search/by-note?note=D%23&scale_type=minor"
```

**Response:**
```json
[
  {
    "symbol": "C",
    "root_note": "C",
    "notes": ["C", "E", "G"],
    "intervals": [0, 4, 7],
    "chord_quality": "major",
    "id": 1,
    "roman_numeral": null,
    "function": null,
    "created_at": "2025-12-29T15:32:10.988714Z"
  },
  {
    "symbol": "Fmaj7",
    "root_note": "F",
    "notes": ["F", "A", "C", "E"],
    "intervals": [0, 4, 7, 11],
    "chord_quality": "major7",
    "id": 18,
    "roman_numeral": null,
    "function": null,
    "created_at": "2025-12-29T15:32:10.988714Z"
  }
]
```

**Features:**
- Handles enharmonic equivalents (C# = D-, D# = E-, etc.)
- Returns all chords in the database containing the specified note
- Scale type parameter for future filtering capabilities

---

### 2. Key Signature Endpoints

#### Get All Key Signatures
```bash
GET /keys/
```

**Query Parameters:**
- `mode` (string, optional): Filter by mode ("major" or "minor")

**Examples:**
```bash
# All key signatures
curl "http://localhost:8000/api/v1/keys/"

# Only major keys
curl "http://localhost:8000/api/v1/keys/?mode=major"

# Only minor keys
curl "http://localhost:8000/api/v1/keys/?mode=minor"
```

**Response:**
```json
[
  {
    "key_name": "C major",
    "tonic": "C",
    "mode": "major",
    "sharps_flats": 0,
    "accidentals": [],
    "scale_notes": ["C", "D", "E", "F", "G", "A", "B", "C"],
    "id": 1,
    "created_at": "2025-12-28T14:01:10.704854Z"
  }
]
```

#### Get Chords for a Key Signature
```bash
GET /keys/{key_name}/chords/
```

**Parameters:**
- `key_name` (string): The key signature name (URL encoded)

**Example:**
```bash
# C major (note the URL encoding of space: %20)
curl "http://localhost:8000/api/v1/keys/C%20major/chords/"

# A minor
curl "http://localhost:8000/api/v1/keys/A%20minor/chords/"
```

**Response:**
```json
[
  {
    "symbol": "C",
    "root_note": "C",
    "notes": ["C", "E", "G"],
    "chord_quality": "major",
    "function": "tonic"
  }
]
```

---

### 3. Reharmonization Endpoints

#### Get Chord Substitutions
```bash
GET /reharmonize/substitutions/{chord_symbol}
```

**Path Parameters:**
- `chord_symbol` (string): The chord to get substitutions for

**Query Parameters:**
- `technique` (string, optional): Substitution technique
  - `random` (default) - Random selection
  - `tritone` - Tritone substitution
  - `diatonic` - Diatonic substitutions
  - `chromatic` - Chromatic approach
  - `circle-of-fifths` - Circle of fifths progression

**Examples:**
```bash
# Random substitutions for C
curl "http://localhost:8000/api/v1/reharmonize/substitutions/C?technique=random"

# Tritone substitutions for Dm
curl "http://localhost:8000/api/v1/reharmonize/substitutions/Dm?technique=tritone"

# Diatonic substitutions for G7
curl "http://localhost:8000/api/v1/reharmonize/substitutions/G7?technique=diatonic"
```

**Response:**
```json
{
  "original_chord": "C",
  "substitutions": [
    {
      "chord": "Am",
      "technique": "random",
      "description": "Random selection from available chords",
      "common_usage": "Alternative to C",
      "score": 1.0
    },
    {
      "chord": "Em",
      "technique": "random",
      "description": "Random selection from available chords",
      "common_usage": "Alternative to C",
      "score": 1.0
    }
  ]
}
```

#### Get Context-Aware Substitutions
```bash
POST /reharmonize/substitutions/analyze/
```

**Request Body:**
```json
{
  "chord": "C",
  "context": {
    "key": "C major",
    "previousChord": "F",
    "nextChord": "G",
    "position": "tonic"
  },
  "techniques": ["tritone", "diatonic"]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/reharmonize/substitutions/analyze/" \
  -H "Content-Type: application/json" \
  -d '{
    "chord": "C",
    "context": {
      "key": "C major",
      "position": "tonic"
    }
  }'
```

**Response:**
```json
{
  "original_chord": "C",
  "substitutions": [
    {
      "chord": "Am",
      "technique": "diatonic",
      "description": "Diatonic substitution within key",
      "common_usage": "Relative minor substitution",
      "score": 0.85
    }
  ]
}
```

---

### 4. Improvisation Endpoints

#### Get Improvisation Notes
```bash
GET /improvisation/notes/{chord_symbol}
```

**Path Parameters:**
- `chord_symbol` (string): The chord to get improvisation notes for

**Query Parameters:**
- `count` (int, optional): Number of recommended notes (default: 5)

**Examples:**
```bash
# Get 5 notes for C
curl "http://localhost:8000/api/v1/improvisation/notes/C?count=5"

# Get 7 notes for G7
curl "http://localhost:8000/api/v1/improvisation/notes/G7?count=7"

# Default count (5)
curl "http://localhost:8000/api/v1/improvisation/notes/Am"
```

**Response:**
```json
{
  "chord_symbol": "C",
  "chord_tones": ["C", "E", "G"],
  "scale_notes": ["C", "D", "E", "F", "G", "A", "B"],
  "recommended_notes": ["C", "E", "G", "A", "B"],
  "avoid_notes": ["F"]
}
```

**Known Issue:**
Chord symbols with quality indicators (m, maj, etc.) may fail to parse:
```json
{
  "chord_symbol": "Dm7",
  "chord_tones": [],
  "scale_notes": [],
  "recommended_notes": [],
  "avoid_notes": [],
  "error": "m is not a supported accidental type"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Not Found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "count"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal Server Error"
}
```

---

## Testing the API

### Using the Test Script

A comprehensive test script is provided:

```bash
# Make it executable
chmod +x test_api.sh

# Run all tests
./test_api.sh

# Run with custom API URL
API_BASE=http://localhost:8000/api/v1 ./test_api.sh
```

### Manual Testing with curl

```bash
# Test basic connectivity
curl http://localhost:8000/docs

# Get all chords (follow redirects)
curl -L http://localhost:8000/api/v1/chords

# Get substitutions with technique
curl "http://localhost:8000/api/v1/reharmonize/substitutions/C?technique=tritone"

# Get improvisation notes
curl "http://localhost:8000/api/v1/improvisation/notes/G7?count=5"

# Pretty print JSON
curl -s "http://localhost:8000/api/v1/chords/" | python3 -m json.tool
```

### Testing with httpie

```bash
# Install httpie
pip install httpie

# Examples
http GET localhost:8000/api/v1/chords/
http GET "localhost:8000/api/v1/reharmonize/substitutions/C" technique==random
http POST localhost:8000/api/v1/reharmonize/substitutions/analyze/ \
  chord=C context:='{"key":"C major"}'
```

---

## Data Models

### Chord
```typescript
interface Chord {
  id: number;
  symbol: string;           // e.g., "C", "Dm7", "G7"
  root_note: string;        // e.g., "C", "D", "G"
  chord_quality: string;    // e.g., "major", "minor", "dominant7"
  notes: string[];          // e.g., ["C", "E", "G"]
  intervals: number[];      // e.g., [0, 4, 7]
  roman_numeral?: string;   // e.g., "I", "ii", "V7"
  function?: string;        // e.g., "tonic", "dominant"
  created_at: string;       // ISO 8601 timestamp
}
```

### KeySignature
```typescript
interface KeySignature {
  id: number;
  key_name: string;         // e.g., "C major", "A minor"
  tonic: string;            // e.g., "C", "A"
  mode: string;             // "major" or "minor"
  sharps_flats: number;     // Positive for sharps, negative for flats
  accidentals: string[];    // e.g., ["F#", "C#"]
  scale_notes: string[];    // e.g., ["C", "D", "E", "F", "G", "A", "B", "C"]
  created_at: string;       // ISO 8601 timestamp
}
```

### SubstitutionOption
```typescript
interface SubstitutionOption {
  chord: string;            // The substitute chord symbol
  technique: string;        // Technique used
  description: string;      // Human-readable description
  common_usage: string;     // When to use this substitution
  score: number;            // Similarity score (0.0 - 1.0)
}
```

### SubstitutionResponse
```typescript
interface SubstitutionResponse {
  original_chord: string;
  substitutions: SubstitutionOption[];
}
```

### ImprovisationNotesResponse
```typescript
interface ImprovisationNotesResponse {
  chord_symbol: string;
  chord_tones: string[];        // Notes in the chord
  scale_notes: string[];        // Notes in the appropriate scale
  recommended_notes: string[];  // Best notes for improvisation
  avoid_notes: string[];        // Notes that may clash
  error?: string;               // Error message if parsing failed
}
```

---

## Known Issues

### 1. Trailing Slash Redirects
**Issue:** Requests without trailing slashes get 307 redirects
**Workaround:** Use `-L` flag with curl or add trailing slashes to URLs

### 2. Music21 Chord Parsing
**Issue:** Chords like "Dm7", "Cmaj7" fail with "m is not a supported accidental type"
**Cause:** music21 doesn't parse these chord symbols correctly
**Status:** Backend returns error in response instead of failing
**Workaround:** Use simple chord symbols like "C", "D", "G"

### 3. Minor Key Filter
**Issue:** `/keys/?mode=minor` returns all keys
**Status:** Backend endpoint needs fixing

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:
- Implement rate limiting middleware
- Use Redis for distributed rate limiting
- Add API keys for authentication

---

## Versioning

The API is versioned through the URL path: `/api/v1/`

Future versions will use:
- `/api/v2/` for breaking changes
- Header-based versioning for non-breaking changes

---

## Support

For issues or questions:
- Check the logs: `docker-compose logs backend`
- Run the test script: `./test_api.sh`
- View API docs: http://localhost:8000/docs
