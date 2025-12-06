# Lottery Lab Development Makefile
.PHONY: help install install-dev clean test test-cov test-fast lint format check db-init db-upgrade db-downgrade server run migrate logs

# Default target
help: ## Show this help message
	@echo "Lottery Lab Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -e ".[dev]"

# Code quality
lint: ## Run linting checks
	flake8 lotterylab tests
	mypy lotterylab

format: ## Format code with black and isort
	black lotterylab tests
	isort lotterylab tests

check: ## Run all code quality checks
	make lint
	make test
	@echo "All checks passed! ✅"

# Testing
test: ## Run all tests
	pytest tests/

test-cov: ## Run tests with coverage report
	pytest --cov=lotterylab --cov-report=html --cov-report=term-missing tests/

test-fast: ## Run tests without coverage (faster)
	pytest -x --tb=short tests/

# Database
db-init: ## Initialize database and run migrations
	alembic upgrade head

db-upgrade: ## Run database migrations
	alembic upgrade head

db-downgrade: ## Downgrade database (one revision)
	alembic downgrade -1

db-revision: ## Create new database migration
	@echo "Creating new migration..."
	@read -p "Migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# Development server
server: ## Start development server
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run: ## Alias for server
	make server

# Data management
ingest: ## Run data ingestion from CSV
	python -m lotterylab.scripts.import_txt

update: ## Fetch and import new draws from MBNet
	python scripts/update_mbnet.py

# Internationalization (i18n)
i18n-extract: ## Extract translatable strings from templates
	pybabel extract -F babel.cfg -o translations/messages.pot .

i18n-init: ## Initialize a new language (usage: make i18n-init LANG=de)
	pybabel init -i translations/messages.pot -d translations -l $(LANG)

i18n-update: ## Update existing translations with new strings
	pybabel update -i translations/messages.pot -d translations

i18n-compile: ## Compile translations to .mo files
	pybabel compile -d translations

# Logging
logs: ## Show recent application logs
	tail -f logs/lotterylab.log

# Cleanup
clean: ## Clean up build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Docker (if we add Docker later)
docker-build: ## Build Docker image
	docker build -t lotterylab .

docker-run: ## Run Docker container
	docker run -p 8000:8000 lotterylab

# Deployment (placeholder for future use)
deploy-dev: ## Deploy to development environment
	@echo "Development deployment not yet configured"

deploy-prod: ## Deploy to production environment
	@echo "Production deployment not yet configured"

# Quick development setup
setup: ## Full development setup (install deps, init DB, run tests)
	make install-dev
	make db-init
	make test
	@echo "Development environment ready! 🚀"
	@echo "Run 'make server' to start the development server"
