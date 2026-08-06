.PHONY: help up down logs db-shell install dev-backend dev-web docs

help:
	@echo "OpenMCP Makefile commands:"
	@echo "Docker Environment:"
	@echo "  up           - Start local Docker environment in the background"
	@echo "  down         - Stop local Docker environment"
	@echo "  logs         - Tail logs from all containers"
	@echo "  db-shell     - Open PostgreSQL shell"
	@echo ""
	@echo "Local Development:"
	@echo "  install      - Install frontend, backend, and docs dependencies"
	@echo "  dev-backend  - Run backend server locally (uvicorn)"
	@echo "  dev-web      - Run web frontend locally (vite)"
	@echo "  docs         - Run mkdocs server locally"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

db-shell:
	docker compose exec db psql -U openmcp_user -d openmcp_db

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt || true
	@echo "Installing web dependencies..."
	cd web && npm install
	@echo "Installing docs dependencies..."
	pip install mkdocs-material || true
	@echo "Installing CLI in dev mode..."
	cd cli && pip install -e .
	@echo "Installing SDK in dev mode..."
	cd sdk && pip install -e .

dev-backend:
	cd backend && uvicorn app.main:app --reload

dev-web:
	cd web && npm run dev

docs:
	mkdocs serve
