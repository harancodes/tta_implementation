#!/bin/sh

# Wait for DB (optional but recommended)
echo "Running migrations..."
python3 lookit/manage.py migrate

echo "Starting server..."
python3 lookit/manage.py runserver 0.0.0.0:8000