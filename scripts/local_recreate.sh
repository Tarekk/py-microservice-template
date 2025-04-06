#!/bin/bash
set -e

echo "Removing existing migration files..."
rm -rf alembic/versions/*

echo "Removing database file..."
rm -f data/api.db

echo "Generating initial migration..."
uv run python -m alembic revision --autogenerate -m "Initial migration"

echo "Running database migrations..."
uv run python -m alembic upgrade head

echo "Loading initial data..."
uv run python -m api.initial_data

echo "Database recreated successfully!"
