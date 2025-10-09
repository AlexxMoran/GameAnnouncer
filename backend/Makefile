.PHONY: help dev migrate makemigrations clean install test format lint

# Variables
PYTHON = uv run python
UVICORN = uv run uvicorn
ALEMBIC = uv run alembic

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development
dev: ## Start development server with hot reload
	$(UVICORN) main:app --host localhost --port 3000 --reload

start: ## Start production server
	$(UVICORN) main:app --host 0.0.0.0 --port 8000

# Database
migrate: ## Apply database migrations
	$(ALEMBIC) upgrade head

makemigrations: ## Create new database migration
	$(ALEMBIC) revision --autogenerate $(if $(MSG),-m "$(MSG)")

db-downgrade: ## Downgrade database by 1 migration
	$(ALEMBIC) downgrade -1

db-reset: ## Reset database (downgrade to base)
	$(ALEMBIC) downgrade base

# Code quality
format: ## Format code with black
	uv run black .

lint: ## Check code with ruff
	uv run ruff check .

# Testing
test: ## Run tests
	$(PYTHON) -m pytest

# Dependencies
install: ## Install dependencies
	uv sync

install-dev: ## Install dev dependencies
	uv sync --dev

# Cleanup
clean: ## Clean cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Docker
docker-up: ## Start docker containers
	docker compose up -d

docker-down: ## Stop docker containers
	docker compose down

docker-logs: ## Show docker logs
	docker compose logs -f

# Full setup for new developers
setup: install migrate ## Full setup for new developers
	@echo "🎉 Setup complete! Run 'make dev' to start development server"
