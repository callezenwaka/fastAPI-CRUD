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
 1027  alembic revision --autogenerate -m "init"
 1028  alembic revision --autogenerate -m "init"
 1029  alembic revision --autogenerate -m "Update database"
 1030  alembic history
 1031  alembic revision --autogenerate -m "Update database"
 1032  alembic upgrade head
 1033  alembic current
 1034  alembic revision --autogenerate -m "Update database"
 1035  alembic stamp head
 1036  alembic current
 1037  alembic revision --autogenerate -m "Update database"
 1038  alembic revision --autogenerate -m "Update user database"
 1039  alembic current
 1040  alembic stamp head
 1041  alembic revision --autogenerate -m "Update user database"
 1042  alembic upgrade head
```

## Resources
- https://jod35.github.io/fastapi-beyond-crud-docs/site/chapter3/
- https://docs.thunderclient.com/features/system-variables
