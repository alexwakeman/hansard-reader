-- Create user
CREATE USER hansard_service WITH PASSWORD 'admin';

-- Create database
CREATE DATABASE hansard;

-- Connect to the hansard database
\c hansard

-- Create schema
CREATE SCHEMA hansard;

-- Grant privileges
GRANT ALL PRIVILEGES ON SCHEMA hansard TO hansard_service;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA hansard TO hansard_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA hansard GRANT ALL PRIVILEGES ON TABLES TO hansard_service;