-- Database initialization script for PostgreSQL
-- This script runs when the PostgreSQL container starts for the first time

-- Create the healthcare database if it doesn't exist
-- (This is already created by POSTGRES_DB environment variable)

-- Set timezone
SET timezone = 'UTC';

-- Create any additional configurations here if needed
-- For example, you could create additional users or set up specific permissions

-- Grant all privileges to the postgres user (default)
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO postgres;
