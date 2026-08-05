.PHONY: help up down logs db-shell redis-shell

help:
	@echo "OpenMCP Makefile commands:"
	@echo "  up           - Start local development environment (PostgreSQL, Redis) in the background"
	@echo "  down         - Stop local development environment"
	@echo "  logs         - Tail logs from all containers"
	@echo "  db-shell     - Open PostgreSQL shell"
	@echo "  redis-shell  - Open Redis shell"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

db-shell:
	docker compose exec postgres psql -U openmcp -d openmcp_dev

redis-shell:
	docker compose exec redis redis-cli
