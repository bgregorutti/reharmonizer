# 1. Drop and recreate schema
docker-compose exec postgres psql -U reharmonizer_user -d reharmonizer -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO reharmonizer_user; GRANT ALL ON SCHEMA public TO public;"

# 2. Reseed the database
docker-compose exec backend python scripts/seed_database.py
docker-compose exec backend python scripts/generate_substitutions.py
