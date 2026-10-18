.PHONY: dev up down test lint logs

up:        ## production-like stack
	docker compose up --build -d

dev:       ## hot-reload stack
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

down:
	docker compose down

logs:
	docker compose logs -f api worker

test:
	cd apps/api && pytest
	cd apps/web && npm test

lint:
	cd apps/api && ruff check .
