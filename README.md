# FastAPI Projects

## To run your application with Docker Compose
```bash
# Start the database
docker-compose up -d

# Rebuild and restart docker
docker-compose down -v && docker-compose up -d

# connect to database
docker-compose exec app-database psql -U app_user -d app_db
# docker exec -it database-app-postgres-1 psql -U app_user -d app_db

# Start the FastAPI app
uvicorn src:app --reload --host 0.0.0.0 --port $PORT
```

## Use thunder client random uuid
```json
{
    "id": "{{#guid}}"
}
```

## Alembic commads
```bash
alembic revision --autogenerate -m "message"
alembic current
alembic stamp head
alembic upgrade head
```

## Test command
```bash
# both the src and test folders are apart
export PYTHONPATH=$(pwd)/src
pytest

# test schemathesis
st run http://localhost:8000/api/v1/openapi.json --experimental=openapi-3.1
st run http://localhost:8000/api/v1/openapi.json --checks all --experimental=openapi-3.1
```

## Resources
- https://jod35.github.io/fastapi-beyond-crud-docs/site/chapter3/
- https://docs.thunderclient.com/features/system-variables
