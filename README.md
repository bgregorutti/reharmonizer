# Reharmonizer

A web application for chord substitution and reharmonization using music theory algorithms.

## Features

### Chord Substitutions
Interactive chord substitution tool with dual input modes:
- **Classical Mode**: Select key signature (30 major/minor keys) to generate diatonic chords
- **Modern Mode**: Input custom chord progressions

**Substitution Techniques:**
- **All Techniques**: Best substitutions combining all methods
- **Diatonic**: Chords sharing common tones within the same key
- **Circle of Fifths**: Chords related by fifth intervals (strong voice leading)
- **Relative Major/Minor**: Same key signature, different tonal center
- **Parallel Major/Minor**: Same root note, different quality (modal interchange)
- **Chromatic Approach**: Approach chords a semitone away (jazz technique)
- **Tritone Substitution**: Dominant 7th chords a tritone apart (jazz technique)

Each chord displays:
- 5 alternative substitution options
- Music notation (VexFlow rendering)
- Improvisation notes with chord tones and scale recommendations

### Reharmonizer (Coming Soon)
Upload a musical phrase and receive chord recommendations based on the melody.

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React 18, TypeScript, Vite, React Router
- **Music Notation**: VexFlow for rendering chord symbols and notes
- **Database**: PostgreSQL 15
- **Development**: Docker, docker-compose

## Project Structure

```
reharmonizer/
├── backend/              # Python/FastAPI backend
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── schemas/     # Pydantic validation schemas
│   │   ├── services/    # Business logic & music theory algorithms
│   │   └── repositories/# Data access layer
│   ├── alembic/         # Database migrations
│   └── scripts/         # Utility scripts (seeding, etc.)
├── frontend/            # React/TypeScript frontend
│   └── src/
│       ├── components/  # React components
│       │   ├── features/    # Feature-specific components
│       │   ├── layout/      # Layout components
│       │   ├── common/      # Reusable components
│       │   └── pages/       # Page components
│       ├── services/    # API client services
│       ├── store/       # Context API state management
│       └── types/       # TypeScript definitions
└── docker-compose.yml   # Development environment
```

## Getting Started

### Prerequisites

- Docker and docker-compose
- Git

### Installation

1. Clone the repository:
```bash
cd /Users/bgregorutti/Documents/git-projects/reharmonizer
```

2. Copy environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Start all services:
```bash
docker-compose up
```

The services will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

### Database Setup

Run migrations and seed the database:

```bash
# Enter the backend container
docker-compose exec backend bash

# Run migrations
alembic upgrade head

# Seed the database with initial data
python scripts/seed_database.py
```

## API Endpoints

Available at `http://localhost:8000/api/v1`:
- `GET /keys` - List available key signatures
- `GET /keys/{key}/chords` - Get diatonic chords for a key
- `POST /reharmonize` - Get chord substitutions
- `GET /improvisation/notes/{chord}` - Get improvisation notes and scales

Interactive API documentation: http://localhost:8000/docs

## Music Theory Approach

The application uses a **database-driven approach** with pre-computed chord substitution relationships:

### Chord Substitution Database
- **15,000+ substitution pairs** covering major music theory techniques
- Each substitution includes technique classification, shared notes, and compatibility scores
- Techniques include: diatonic, tritone, circle of fifths, chromatic, relative/parallel modal interchange

### Substitution Algorithm
1. Query database for substitutions matching selected technique
2. Filter by compatibility criteria (shared notes, voice leading quality)
3. Return top 5 ranked substitutions
4. Display with music notation and improvisation notes

### Improvisation Notes
- Extract chord tones (root, third, fifth, seventh)
- Determine appropriate scales based on chord quality
- Provide scale recommendations and tension notes

See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for future enhancements and roadmap.

## License

MIT License

## Acknowledgments

- **VexFlow**: Music notation rendering library
- **FastAPI**: Modern Python web framework
- **React**: UI library
