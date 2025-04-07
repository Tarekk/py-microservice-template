#!/bin/bash
set -e  # Exit on any error

# Create data directory if it doesn't exist
mkdir -p /app/data

# Set the SQLite database path in the container's work directory
DB_PATH="/app/data/api.db"

# Check if .env file exists and load it
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Check if the database exists
if [ ! -f "$DB_PATH" ]; then
    echo "Database not found, creating empty database at $DB_PATH..."
    touch "$DB_PATH"
fi

# Check DB_INIT_MODE environment variable and take appropriate action
if [ "$DB_INIT_MODE" = "MIGRATE" ]; then
    echo "Running database migrations..."
    alembic revision --autogenerate -m "Auto migration"
    alembic upgrade head
elif [ "$DB_INIT_MODE" = "RECREATE" ]; then
    echo "Recreating database and resetting migrations..."
    rm -f "$DB_PATH"
    touch "$DB_PATH"
    # Reset alembic by removing all versions and creating a new base
    rm -rf /app/src/alembic/versions/*
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
elif [ "$DB_INIT_MODE" = "NONE" ]; then
    echo "Skipping database initialization (DB_INIT_MODE=NONE)"
else
    echo "Unknown DB_INIT_MODE: $DB_INIT_MODE. Valid options are: NONE, MIGRATE, RECREATE"
fi

python -m src.initial_data

# Execute the command passed to the entrypoint script
echo "Starting application with command: $@"
exec "$@"