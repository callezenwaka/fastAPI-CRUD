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

## Resources
- https://jod35.github.io/fastapi-beyond-crud-docs/site/chapter3/
- https://docs.thunderclient.com/features/system-variables