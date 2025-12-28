# Reharmonizer - Music Reharmonization Web Application

A comprehensive web application for music reharmonization, chord substitution, and improvisation suggestions using music theory algorithms.

## Features

- **Key Signature to Chords**: Get diatonic chord suggestions from key signatures
- **Chord Substitutions**: Advanced reharmonization with:
  - Tritone substitutions
  - Diatonic substitutions
  - Circle of fifths progressions
  - Chromatic approach chords
- **Chord to Notes**: Improvisation helper showing chord tones, scales, tensions, and avoid notes
- **Music Notation**: Visual rendering with VexFlow
- **MusicXML Support**: Import and export progressions

## Tech Stack

- **Backend**: Python 3.11, FastAPI, music21, SQLAlchemy, PostgreSQL
- **Frontend**: React 18, TypeScript, Vite, VexFlow
- **Database**: PostgreSQL 15
- **Development**: Docker, docker-compose

## Project Structure

```
reharmonizer/
├── backend/              # Python/FastAPI backend
│   ├── app/             # Application code
│   ├── alembic/         # Database migrations
│   ├── scripts/         # Utility scripts
│   └── tests/           # Tests
├── frontend/            # React/TypeScript frontend
│   └── src/            # Source code
├── docker/             # Docker configuration
└── docker-compose.yml  # Development environment
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

## Development

### Backend

The backend uses FastAPI with the following structure:
- **models/**: SQLAlchemy ORM models
- **schemas/**: Pydantic schemas for validation
- **api/**: REST API endpoints
- **services/**: Business logic layer
- **repositories/**: Data access layer

API endpoints are available at `/api/v1`:
- `/chords` - Chord operations
- `/keys` - Key signature operations
- `/reharmonize` - Reharmonization endpoints

### Frontend

The frontend uses React with TypeScript:
- **components/**: React components (features, layout, common)
- **hooks/**: Custom React hooks
- **services/**: API client services
- **store/**: Context API state management
- **types/**: TypeScript type definitions

### Running Tests

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## Implementation Status

### Phase 1: Foundation ✅ (Completed)
- ✅ Project structure created
- ✅ Backend skeleton with FastAPI
- ✅ Frontend skeleton with Vite + React + TypeScript
- ✅ Docker configuration
- ✅ Database schema and migrations
- ✅ Seed scripts

### Phase 2: Music Theory Core (Next)
- ⏳ music21 integration
- ⏳ Music theory services
- ⏳ Chord analyzer
- ⏳ Scale generator

### Phase 3: Key Signature to Chords
- ⏳ Backend API implementation
- ⏳ Frontend components
- ⏳ VexFlow integration

### Phase 4: Chord Substitutions
- ⏳ Substitution algorithms
- ⏳ Reharmonization engine
- ⏳ Frontend integration

### Phase 5: Chord to Notes
- ⏳ Improvisation notes calculation
- ⏳ Frontend display

### Phase 6: MusicXML Support
- ⏳ Import/export functionality

### Phase 7: Polish & Testing
- ⏳ UI/UX improvements
- ⏳ Comprehensive testing
- ⏳ Documentation

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## Contributing

This is a project in active development. Features are being implemented according to the roadmap above.

## Music Theory Concepts

The application implements several music theory concepts:

- **Tritone Substitution**: Replace V7 with bII7 (dominant chords a tritone apart)
- **Diatonic Substitution**: Substitute chords within a key (I ↔ iii, ii ↔ IV)
- **Circle of Fifths**: Add ii-V progressions, extend using fifth relationships
- **Chromatic Approach**: Add chromatic chords that lead into target chords

## License

[Add your license here]

## Acknowledgments

- **music21**: Python toolkit for computer-aided musicology
- **VexFlow**: Music notation rendering library
- **FastAPI**: Modern Python web framework
- **React**: UI library
