# Docker Setup Guide

## Architecture

The application uses a multi-container Docker setup with:
- **PostgreSQL**: Database
- **Backend**: Python/FastAPI application with reharmonizer-core
- **Frontend**: React/TypeScript with Vite

## Build Context

The backend Dockerfile uses the **root directory** as the build context to access both:
- `backend/` - FastAPI application code
- `reharmonizer-core/` - Core music theory package

This allows the Dockerfile to copy and install the core package before installing the backend dependencies.

## Building the Application

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend

# Build without cache (for clean rebuild)
docker-compose build --no-cache backend
```

## Running the Application

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Development Workflow

### Backend Changes

The backend code is mounted as a volume, so changes are reflected immediately with hot-reload:

```yaml
volumes:
  - ./backend:/app
  - ./reharmonizer-core:/app/reharmonizer-core
```

**Important**: Changes to `reharmonizer-core` are also reflected immediately since it's installed in editable mode (`pip install -e`).

### Rebuilding After Dependency Changes

If you modify `requirements.txt` or `reharmonizer-core/pyproject.toml`:

```bash
# Rebuild backend container
docker-compose build backend

# Restart backend service
docker-compose up -d backend
```

## Local Development (Outside Docker)

If you want to run the backend locally without Docker:

```bash
# Install core package in editable mode
cd reharmonizer-core
pip install -e .

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Run the backend
uvicorn app.main:app --reload
```

## Troubleshooting

### Error: "reharmonizer_core module not found"

This means the core package wasn't installed properly. Rebuild the container:

```bash
docker-compose build --no-cache backend
docker-compose up backend
```

### Error: "COPY failed"

Check that the build context in `docker-compose.yml` is set to `.` (root directory):

```yaml
backend:
  build:
    context: .  # Root directory, not ./backend
    dockerfile: docker/backend.Dockerfile
```

### Changes to core package not reflected

The core package is mounted as a volume and installed in editable mode, so changes should be reflected immediately. If not:

1. Restart the backend container: `docker-compose restart backend`
2. If still not working, rebuild: `docker-compose build backend && docker-compose up backend`

## Database Setup

```bash
# Enter backend container
docker-compose exec backend bash

# Run migrations
alembic upgrade head

# Seed database
python scripts/seed_database.py

# Exit container
exit
```

## Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend
```

## Cleaning Up

```bash
# Stop and remove containers
docker-compose down

# Remove containers and volumes (WARNING: deletes database)
docker-compose down -v

# Remove containers, volumes, and images
docker-compose down -v --rmi all
```
