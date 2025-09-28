.PHONY: up down logs api web test

up:
docker compose -f docker/docker-compose.yml up -d --build

down:
docker compose -f docker/docker-compose.yml down

logs:
docker compose -f docker/docker-compose.yml logs -f

api:
uvicorn api.main:app --reload

web:
cd web && npm run dev

test:
pytest
