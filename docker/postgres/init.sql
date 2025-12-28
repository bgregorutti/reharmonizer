-- Initialize the reharmonizer database
-- This script runs when the container is first created

\c reharmonizer

-- Create extensions if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Database is ready
SELECT 'Database initialized successfully' AS status;
