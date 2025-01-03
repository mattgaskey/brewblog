#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database to start..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

# Run database migrations
echo "Running database migrations..."

if flask db upgrade; then
  echo "Database migrations completed successfully"
else
  echo "Database migrations failed"
  exit 1
fi

# Debug: Check the Python environment and installed packages
echo "Checking Python environment..."
python -c "import sys; print(sys.executable)"
python -m pip list

# Seed the database using the virtual environment's Python interpreter
echo "Seeding the database..."
python seed.py

# Start your Flask application
echo "Starting Flask application..."
exec flask run --host=0.0.0.0 --reload