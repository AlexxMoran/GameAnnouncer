.PHONY: help project-up project-down project-logs project-shell project-reset project-rebuild project-status

# Variables
COMPOSE = docker compose
BACKEND_ENV_FILE = backend/.env
BACKEND_ENV_TEMPLATE = backend/.env.template

# Default target
help: ## Show this help message
	@echo "🚀 GameAnnouncer - Project Management Commands"
	@echo "=============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 For backend development commands, go to backend/ folder and run 'make help'"

# Check and create .env file if needed
check-backend-env:
	@if [ ! -f $(BACKEND_ENV_FILE) ]; then \
		echo "📋 Creating backend .env from template..."; \
		if [ -f $(BACKEND_ENV_TEMPLATE) ]; then \
			cp $(BACKEND_ENV_TEMPLATE) $(BACKEND_ENV_FILE); \
			echo "✅ Created $(BACKEND_ENV_FILE) from template"; \
		else \
			echo "⚠️  Please create $(BACKEND_ENV_FILE) file manually"; \
			echo "Example content:"; \
			echo "DB__USER=postgres"; \
			echo "DB__PASSWORD=postgres"; \
			echo "DB__DATABASE=game_announcer"; \
			exit 1; \
		fi; \
	fi

# Project Management - Docker Commands
project-up: backend-up frontend-up ## 🚀 Complete setup - build and start everything!
	@echo "🚀 Starting full GameAnnouncer development environment..."
	@echo ""
	@echo "🎉 Ready! Your full development environment is running:"
	@echo "🎨 Frontend: http://localhost:4200"
	@echo "📱 API: http://localhost:3000"
	@echo "📊 Docs: http://localhost:3000/docs"
	@echo "📧 Mailpit: http://localhost:8025"

project-down: ## 🛑 Stop all containers
	@echo "🛑 Stopping GameAnnouncer containers..."
	$(COMPOSE) down

project-rebuild: check-backend-env ## 🔨 Force rebuild and restart containers
	@echo "🔨 Force rebuilding containers..."
	$(COMPOSE) up --build -d

project-logs: ## 📊 Show all services logs
	$(COMPOSE) logs -f

project-logs-backend: ## 📊 Show backend logs
	$(COMPOSE) logs -f backend

project-logs-all: ## 📊 Show all containers logs
	$(COMPOSE) logs -f

project-shell: ## 🐚 Get shell in backend container
	$(COMPOSE) exec backend bash

project-db-shell: ## 🗄️ Get PostgreSQL shell
	$(COMPOSE) exec db psql -U postgres -d game_announcer

project-status: ## 📋 Show containers status
	@echo "📋 GameAnnouncer containers status:"
	$(COMPOSE) ps

project-reset: check-backend-env ## 🧹 Reset everything and restart (removes all data!)
	@echo "🧹 Resetting development environment..."
	@echo "⚠️  This will remove all database data!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		$(COMPOSE) down -v; \
		$(COMPOSE) up --build -d; \
		echo "⏳ Waiting for database..."; \
		timeout=60; \
		while ! $(COMPOSE) exec -T db pg_isready -U postgres >/dev/null 2>&1; do \
			sleep 2; \
			timeout=$$((timeout - 2)); \
			if [ $$timeout -le 0 ]; then \
				echo "❌ Database timeout"; \
				exit 1; \
			fi; \
		done; \
		$(COMPOSE) exec backend uv run alembic upgrade head; \
		echo "🎉 Environment reset complete!"; \
	else \
		echo "❌ Reset cancelled"; \
	fi

# Configuration commands
config: check-backend-env ## 🔧 Show docker-compose configuration
	$(COMPOSE) --env-file backend/.env config

validate: check-backend-env ## ✅ Validate docker-compose configuration
	$(COMPOSE) --env-file backend/.env config --quiet && echo "✅ Configuration is valid"

# Backend and DB only (without frontend)
backend-up: check-backend-env ## 🔧 Start only backend and database
	@echo "🔧 Starting backend services (DB + Redis + Mailpit + API + Worker + Scheduler)..."
	@echo "📦 Checking container status..."
	@db_running=$$($(COMPOSE) --env-file backend/.env ps -q db 2>/dev/null | wc -l | tr -d ' '); \
	redis_running=$$($(COMPOSE) --env-file backend/.env ps -q redis 2>/dev/null | wc -l | tr -d ' '); \
	mailpit_running=$$($(COMPOSE) --env-file backend/.env ps -q mailpit 2>/dev/null | wc -l | tr -d ' '); \
	backend_running=$$($(COMPOSE) --env-file backend/.env ps -q backend 2>/dev/null | wc -l | tr -d ' '); \
	worker_running=$$($(COMPOSE) --env-file backend/.env ps -q worker 2>/dev/null | wc -l | tr -d ' '); \
	scheduler_running=$$($(COMPOSE) --env-file backend/.env ps -q scheduler 2>/dev/null | wc -l | tr -d ' '); \
	services_to_start=""; \
	if [ "$$db_running" -eq 0 ]; then \
		echo "📊 Database not running, will start it"; \
		services_to_start="$$services_to_start db"; \
	else \
		echo "✅ Database already running"; \
	fi; \
	if [ "$$redis_running" -eq 0 ]; then \
		echo "🔴 Redis not running, will start it"; \
		services_to_start="$$services_to_start redis"; \
	else \
		echo "✅ Redis already running"; \
	fi; \
	if [ "$$mailpit_running" -eq 0 ]; then \
		echo "📧 Mailpit not running, will start it"; \
		services_to_start="$$services_to_start mailpit"; \
	else \
		echo "✅ Mailpit already running"; \
	fi; \
	if [ "$$backend_running" -eq 0 ]; then \
		echo "🔧 Backend not running, will start it"; \
		services_to_start="$$services_to_start backend"; \
	else \
		echo "✅ Backend already running"; \
	fi; \
	if [ "$$worker_running" -eq 0 ]; then \
		echo "⚙️  Worker not running, will start it"; \
		services_to_start="$$services_to_start worker"; \
	else \
		echo "✅ Worker already running"; \
	fi; \
	if [ "$$scheduler_running" -eq 0 ]; then \
		echo "🕐 Scheduler not running, will start it"; \
		services_to_start="$$services_to_start scheduler"; \
	else \
		echo "✅ Scheduler already running"; \
	fi; \
	if [ -n "$$services_to_start" ]; then \
		echo "🚀 Starting:$$services_to_start"; \
		$(COMPOSE) --env-file backend/.env up -d$$services_to_start; \
		echo "⏳ Waiting for services to be ready..."; \
		sleep 5; \
	else \
		echo "🎉 All backend services already running!"; \
	fi
	@echo "⏳ Waiting for database to accept connections..."
	@timeout=90; \
	while ! $(COMPOSE) --env-file backend/.env exec -T db pg_isready -U postgres >/dev/null 2>&1; do \
		sleep 3; \
		timeout=$$((timeout - 3)); \
		if [ $$timeout -le 0 ]; then \
			echo "❌ Database timeout after 90 seconds"; \
			exit 1; \
		fi; \
		echo "⏳ Still waiting for database... ($$timeout seconds left)"; \
	done
	@echo "⏳ Waiting for Redis to accept connections..."
	@timeout=30; \
	while ! $(COMPOSE) --env-file backend/.env exec -T redis redis-cli ping >/dev/null 2>&1; do \
		sleep 2; \
		timeout=$$((timeout - 2)); \
		if [ $$timeout -le 0 ]; then \
			echo "❌ Redis timeout after 30 seconds"; \
			exit 1; \
		fi; \
		echo "⏳ Still waiting for Redis... ($$timeout seconds left)"; \
	done
	@echo "📊 Running migrations..."
	@$(COMPOSE) --env-file backend/.env exec backend uv run alembic upgrade head
	@echo "✅ Backend services ready!"

backend-down: ## 🛑 Stop only backend services
	$(COMPOSE) stop backend worker db redis mailpit

backend-logs: ## 📊 Show backend services logs
	$(COMPOSE) logs -f backend worker db redis mailpit

# Frontend Management
frontend-up: ## 🎨 Start only frontend services
	@echo "🎨 Starting frontend services..."
	@echo "📦 Checking frontend container status..."
	@frontend_running=$$($(COMPOSE) ps -q frontend 2>/dev/null | wc -l | tr -d ' '); \
	if [ "$$frontend_running" -eq 0 ]; then \
		echo "🎨 Frontend not running, will start it"; \
		echo "🚀 Starting frontend..."; \
		$(COMPOSE) up -d frontend; \
		echo "⏳ Waiting for frontend to be ready..."; \
		sleep 10; \
		echo "✅ Frontend services ready!"; \
		echo "🎉 Frontend running at: http://localhost:4200"; \
	else \
		echo "✅ Frontend already running"; \
		echo "🎉 Frontend available at: http://localhost:4200"; \
	fi

frontend-down: ## 🛑 Stop only frontend services
	$(COMPOSE) stop frontend

frontend-logs: ## 📊 Show frontend services logs
	$(COMPOSE) logs -f frontend

# Quick shortcuts for common actions
up: project-up ## Alias for project-up
down: project-down ## Alias for project-down
logs: project-logs ## Alias for project-logs
shell: project-shell ## Alias for project-shell
status: project-status ## Alias for project-status

# Development shortcuts - proxy to backend Makefile
dev: ## 🔧 Start backend development server (local)
	@echo "🔧 Starting backend development server..."
	@cd backend && make dev

migrate: ## 📊 Apply database migrations
	@cd backend && make migrate

makemigrations: ## 📝 Create new database migration
	@cd backend && make makemigrations MSG="$(MSG)"

test: ## 🧪 Run backend tests
	@cd backend && make test

format: ## 🎨 Format backend code
	@cd backend && make format

lint: ## 🔍 Lint backend code
	@cd backend && make lint

install: ## 📦 Install backend dependencies
	@cd backend && make install
