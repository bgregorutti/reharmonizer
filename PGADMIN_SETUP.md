# pgAdmin Setup Guide

## Overview

pgAdmin 4 is included in the Docker Compose setup for database management. It provides a web-based interface to manage the PostgreSQL database.

## Access Information

- **URL**: http://localhost:5050
- **Email**: admin@reharmonizer.com
- **Password**: SecurePassword123

## Configuration

The pgAdmin service is configured in `docker-compose.yml`:

```yaml
pgadmin:
  image: "dpage/pgadmin4:8"
  container_name: reharmonizer-pgadmin
  environment:
    - PGADMIN_DEFAULT_EMAIL=admin@reharmonizer.com
    - PGADMIN_DEFAULT_PASSWORD=SecurePassword123
  ports:
    - 5050:80
  networks:
    - reharmonizer-network
  volumes:
    - ./volumes/pgadmin:/var/lib/pgadmin
  depends_on:
    postgres:
      condition: service_healthy
  profiles:
    - admin
```

## Starting pgAdmin

### Option 1: With Profile (Recommended)
```bash
docker-compose --profile admin up -d pgadmin
```

### Option 2: Without Profile
Remove the `profiles:` section from docker-compose.yml, then:
```bash
docker-compose up -d pgadmin
```

## Connecting to the Database

Once logged into pgAdmin:

1. **Right-click "Servers"** → **Register** → **Server**

2. **General Tab**:
   - Name: `Reharmonizer Database`

3. **Connection Tab**:
   - Host name/address: `postgres` (the service name in docker-compose)
   - Port: `5432`
   - Maintenance database: `reharmonizer`
   - Username: `reharmonizer_user`
   - Password: `dev_password`
   - Save password: ✓ (optional)

4. **Click "Save"**

## Common Issues and Solutions

### Issue: KeyError 'auth_source_manager'

**Symptoms:**
- pgAdmin returns 500 error
- Logs show: `KeyError: 'auth_source_manager'`

**Cause:**
Corrupted session data in the persistent volume, often happens when:
- pgAdmin version is upgraded
- Volume data is incompatible
- Previous session data is malformed

**Solution:**
```bash
# Stop pgAdmin
docker-compose stop pgadmin

# Clear the volume data
rm -rf volumes/pgadmin
mkdir -p volumes/pgadmin

# Restart pgAdmin
docker-compose up -d pgadmin

# Wait a few seconds for initialization
sleep 10

# Access at http://localhost:5050
```

### Issue: Cannot Connect to Database

**Check 1: Verify PostgreSQL is running**
```bash
docker-compose ps postgres
```

**Check 2: Test PostgreSQL connection**
```bash
docker-compose exec postgres psql -U reharmonizer_user -d reharmonizer -c "SELECT 1;"
```

**Check 3: Verify network connectivity**
```bash
docker-compose exec pgadmin ping postgres
```

**Solution:**
Ensure you're using the correct hostname:
- Use `postgres` (service name), NOT `localhost`
- Use `5432` (internal port), NOT the exposed port

### Issue: Permission Denied on volumes/pgadmin

**Solution:**
```bash
# Fix permissions
chmod -R 755 volumes/pgadmin

# Or recreate with proper permissions
docker-compose down pgadmin
rm -rf volumes/pgadmin
docker-compose up -d pgadmin
```

## Volume Management

The pgAdmin configuration and sessions are stored in:
```
./volumes/pgadmin/
```

**Important:** This directory should be in `.gitignore` to avoid committing:
- Session data
- Saved passwords
- User preferences
- Server configurations

To reset pgAdmin completely:
```bash
docker-compose down pgadmin
rm -rf volumes/pgadmin
docker-compose up -d pgadmin
```

## Database Tables

Once connected, you can explore:

- **chords** - Chord definitions with symbols, notes, intervals
- **key_signatures** - Key signatures with scale notes and accidentals
- **substitution_rules** - Chord substitution rules
- **reharmonization_patterns** - Reharmonization patterns

## Useful Queries

### View all chords
```sql
SELECT symbol, root_note, chord_quality, notes
FROM chords
ORDER BY symbol;
```

### View all key signatures
```sql
SELECT key_name, tonic, mode, sharps_flats, scale_notes
FROM key_signatures
ORDER BY sharps_flats;
```

### Count chords by quality
```sql
SELECT chord_quality, COUNT(*) as count
FROM chords
GROUP BY chord_quality
ORDER BY count DESC;
```

## Profiles Feature

The pgAdmin service uses Docker Compose profiles, which means:
- It won't start with `docker-compose up` by default
- Use `docker-compose --profile admin up` to include it
- This keeps the development environment lightweight

To make pgAdmin start by default, remove these lines from docker-compose.yml:
```yaml
profiles:
  - admin
```

## Security Notes

**Development Environment:**
- Default credentials are hardcoded for convenience
- Volume data is local and not production-grade

**Production Environment:**
- Use strong, unique passwords
- Store credentials in environment variables or secrets
- Use SSL/TLS for connections
- Restrict network access
- Use proper volume backups
- Consider using managed database services

## Troubleshooting

### Check pgAdmin logs
```bash
docker-compose logs pgadmin
```

### Check if pgAdmin is responding
```bash
curl -I http://localhost:5050
```

### Restart pgAdmin
```bash
docker-compose restart pgadmin
```

### Force rebuild
```bash
docker-compose down pgadmin
docker-compose up -d --force-recreate pgadmin
```

## Resources

- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [Docker pgAdmin Image](https://hub.docker.com/r/dpage/pgadmin4)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
