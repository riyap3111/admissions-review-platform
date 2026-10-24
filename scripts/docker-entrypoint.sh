#!/bin/sh
# Runs pending Alembic migrations, then starts the API — standard practice
# for a containerized backend with its own migration history. Respects an
# explicit command override (e.g. `docker compose run api bash ...`) via
# the usual entrypoint-script convention.
set -e

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

echo "Running database migrations..."
alembic upgrade head

PORT="${PORT:-8010}"
exec uvicorn admissions_platform.api.main:app --host 0.0.0.0 --port "$PORT"
